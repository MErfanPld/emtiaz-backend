from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from real_estate.models import Property

from .forms import PropertyForm, PropertyImageFormSet


class ApprovedRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_active:
            return redirect('accounts:login')
        if not getattr(request.user, 'is_approved', False):
            return redirect('accounts:pending')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class DashboardIndexView(ApprovedRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = Property.objects.all()
        ctx['property_total'] = qs.count()
        ctx['property_active'] = qs.filter(is_active=True).count()
        ctx['property_draft'] = qs.filter(is_active=False).count()
        ctx['recent_properties'] = qs.order_by('-created_at')[:8]
        return ctx


@method_decorator(login_required, name='dispatch')
class PropertyDashboardListView(ApprovedRequiredMixin, ListView):
    model = Property
    template_name = 'dashboard/property_list.html'
    context_object_name = 'properties'
    paginate_by = 20

    def get_queryset(self):
        qs = Property.objects.all().order_by('-created_at')
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
            qs = qs.filter(is_active=True)
        elif status == 'draft':
            qs = qs.filter(is_active=False)
        return qs


class PropertyFormsetMixin:
    """ذخیره فرم اصلی + formset گالری."""

    def get_formset(self):
        if self.request.method == 'POST':
            return PropertyImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=getattr(self, 'object', None),
            )
        return PropertyImageFormSet(instance=getattr(self, 'object', None))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'formset' not in ctx:
            ctx['formset'] = self.get_formset()
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        # برای create ابتدا object را بساز
        self.object = form.save()
        formset = PropertyImageFormSet(
            self.request.POST,
            self.request.FILES,
            instance=self.object,
        )
        if formset.is_valid():
            formset.save()
            messages.success(self.request, self.success_message)
            return redirect(self.get_success_url())
        # formset نامعتبر — دوباره نمایش
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


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

    def form_valid(self, form):
        messages.success(self.request, 'ملک حذف شد.')
        return super().form_valid(form)
