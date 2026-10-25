import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from blog.models import Category, Post, Tag
from core.models import ConsultationRequest
from core.neighborhoods import TEHRAN_NEIGHBORHOODS
from real_estate.models import Property

from .forms import PropertyForm, PropertyImageFormSet

User = get_user_model()


class ApprovedRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_active:
            return redirect('accounts:login')
        if not getattr(request.user, 'is_approved', False):
            return redirect('accounts:pending')
        return super().dispatch(request, *args, **kwargs)


class StaffManagerMixin(ApprovedRequiredMixin):
    """فقط مدیر / سوپریوزر."""

    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        if hasattr(resp, 'status_code') and resp.status_code in (301, 302):
            return resp
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'دسترسی فقط برای مدیران.')
            return redirect('dashboard:index')
        return resp


def _user_properties_qs(user):
    """کاربر عادی فقط املاک خودش؛ مدیر همه."""
    qs = Property.objects.all().order_by('-created_at')
    if user.is_staff or user.is_superuser:
        return qs
    return qs.filter(created_by=user)


@method_decorator(login_required, name='dispatch')
class DashboardIndexView(ApprovedRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        props = _user_properties_qs(user)
        ctx['property_total'] = props.count()
        ctx['property_active'] = props.filter(
            is_active=True, publish_status=Property.PublishStatus.APPROVED
        ).count()
        ctx['property_pending'] = props.filter(
            publish_status=Property.PublishStatus.PENDING
        ).count()
        ctx['property_draft'] = props.filter(
            publish_status=Property.PublishStatus.REJECTED
        ).count()
        ctx['recent_properties'] = props.order_by('-created_at')[:5]

        is_manager = user.is_staff or user.is_superuser
        ctx['is_manager'] = is_manager

        if is_manager:
            posts = Post.objects.all()
            ctx['post_total'] = posts.count()
            ctx['post_published'] = posts.filter(is_published=True).count()
            ctx['post_draft'] = posts.filter(is_published=False).count()
            ctx['post_views'] = posts.aggregate(total=Sum('views_count'))['total'] or 0
            ctx['category_count'] = Category.objects.count()
            ctx['tag_count'] = Tag.objects.count()
            ctx['recent_posts'] = posts.select_related('category').order_by('-created_at')[:5]
            ctx['consultation_new'] = ConsultationRequest.objects.filter(
                status=ConsultationRequest.Status.NEW
            ).count()
            ctx['user_total'] = User.objects.count()
            ctx['user_pending'] = User.objects.filter(
                approval_status=User.ApprovalStatus.PENDING
            ).count()
            ctx['user_approved'] = User.objects.filter(
                approval_status=User.ApprovalStatus.APPROVED
            ).count()
        else:
            ctx['post_total'] = 0
            ctx['post_published'] = 0
            ctx['post_draft'] = 0
            ctx['post_views'] = 0
            ctx['category_count'] = 0
            ctx['tag_count'] = 0
            ctx['recent_posts'] = []
            ctx['consultation_new'] = 0

        return ctx


@method_decorator(login_required, name='dispatch')
class NotificationsView(ApprovedRequiredMixin, TemplateView):
    template_name = 'dashboard/notifications.html'

    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        if hasattr(resp, 'status_code') and resp.status_code in (301, 302):
            return resp
        # اعلانات مدیریتی فقط برای مدیر
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'دسترسی به اعلانات فقط برای مدیران است.')
            return redirect('dashboard:index')
        return resp

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pending_properties'] = (
            Property.objects.filter(publish_status=Property.PublishStatus.PENDING)
            .select_related('created_by')
            .order_by('-created_at')[:30]
        )
        ctx['new_consultations'] = (
            ConsultationRequest.objects.filter(status=ConsultationRequest.Status.NEW)
            .order_by('-created_at')[:30]
        )
        ctx['is_manager'] = True
        return ctx


@method_decorator(login_required, name='dispatch')
class PropertyDashboardListView(ApprovedRequiredMixin, ListView):
    model = Property
    template_name = 'dashboard/property_list.html'
    context_object_name = 'properties'
    paginate_by = 20

    def get_queryset(self):
        qs = _user_properties_qs(self.request.user)
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(code__icontains=q)
                | Q(title__icontains=q)
                | Q(title_en__icontains=q)
                | Q(area_name__icontains=q)
            )
        status = self.request.GET.get('status')
        if status == 'active':
            qs = qs.filter(is_active=True, publish_status=Property.PublishStatus.APPROVED)
        elif status == 'pending':
            qs = qs.filter(publish_status=Property.PublishStatus.PENDING)
        elif status == 'draft':
            qs = qs.filter(publish_status=Property.PublishStatus.REJECTED)
        return qs


class PropertyFormsetMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_formset(self, instance=None):
        if instance is None:
            instance = getattr(self, 'object', None)
        if self.request.method == 'POST':
            return PropertyImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=instance,
            )
        return PropertyImageFormSet(instance=instance)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'formset' not in ctx:
            ctx['formset'] = self.get_formset()
        ctx['neighborhood_map'] = TEHRAN_NEIGHBORHOODS
        ctx['neighborhood_map_json'] = json.dumps(TEHRAN_NEIGHBORHOODS, ensure_ascii=False)
        return ctx

    def form_valid(self, form):
        with transaction.atomic():
            is_create = form.instance.pk is None
            self.object = form.save(commit=False)
            if is_create:
                self.object.created_by = self.request.user
                if self.request.user.is_staff or self.request.user.is_superuser:
                    self.object.publish_status = Property.PublishStatus.APPROVED
                    self.object.is_active = True
                else:
                    self.object.publish_status = Property.PublishStatus.PENDING
                    self.object.is_active = False
            self.object.save()
            form.save_m2m()

            formset = PropertyImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
            )
            if not formset.is_valid():
                transaction.set_rollback(True)
                messages.error(
                    self.request,
                    'خطا در گالری تصاویر. ردیف‌های خالی را خالی بگذارید یا فیلدها را کامل کنید.',
                )
                return self.render_to_response(
                    self.get_context_data(form=form, formset=formset)
                )
            formset.save()

        if is_create and self.object.publish_status == Property.PublishStatus.PENDING:
            messages.success(
                self.request,
                'ملک ثبت شد و در انتظار تأیید مدیر برای انتشار است.',
            )
        else:
            messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class PropertyCreateView(ApprovedRequiredMixin, PropertyFormsetMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'dashboard/property_form.html'
    success_url = reverse_lazy('dashboard:property_list')
    success_message = 'ملک با موفقیت ثبت شد.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'افزودن ملک جدید'
        ctx['submit_label'] = 'ثبت ملک'
        if 'formset' not in kwargs:
            ctx['formset'] = PropertyImageFormSet()
        return ctx


@method_decorator(login_required, name='dispatch')
class PropertyUpdateView(ApprovedRequiredMixin, PropertyFormsetMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'dashboard/property_form.html'
    success_url = reverse_lazy('dashboard:property_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_message = 'تغییرات ملک و گالری ذخیره شد.'

    def get_queryset(self):
        return _user_properties_qs(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'ویرایش ملک — {self.object.code}'
        ctx['submit_label'] = 'ذخیره تغییرات'
        return ctx


@method_decorator(login_required, name='dispatch')
class PropertyDeleteView(ApprovedRequiredMixin, DeleteView):
    model = Property
    template_name = 'dashboard/property_confirm_delete.html'
    success_url = reverse_lazy('dashboard:property_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return _user_properties_qs(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'ملک حذف شد.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PropertyApproveView(StaffManagerMixin, View):
    def post(self, request, slug):
        prop = get_object_or_404(Property, slug=slug)
        action = request.POST.get('action', 'approve')
        note = request.POST.get('note', '').strip()
        if action == 'reject':
            prop.reject_publish(request.user, note=note)
            messages.warning(request, f'ملک {prop.code} رد شد.')
        else:
            prop.approve_publish(request.user, note=note)
            messages.success(request, f'ملک {prop.code} تأیید و منتشر شد.')
        next_url = request.POST.get('next') or reverse_lazy('dashboard:notifications')
        return redirect(next_url)
