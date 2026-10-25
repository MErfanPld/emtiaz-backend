from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import get_language
from django.views.generic import TemplateView

from real_estate.models import Property

from .forms import ConsultationForm
from .models import TeamMember
from .sms import notify_admins_new_consultation


def _lang_is_en():
    return (get_language() or 'fa')[:2] == 'en'


class HomeView(TemplateView):
    """صفحه اصلی + ثبت درخواست مشاوره."""

    def get_template_names(self):
        if _lang_is_en():
            return ['core/home_en.html']
        return ['core/home.html']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        featured = (
            Property.objects.filter(
                is_active=True,
                publish_status=Property.PublishStatus.APPROVED,
            )
            .order_by('-is_featured', '-created_at')[:8]
        )
        ctx['featured_properties'] = featured
        ctx['property_count'] = Property.objects.filter(
            is_active=True,
            publish_status=Property.PublishStatus.APPROVED,
        ).count()
        ctx['directors'] = (
            TeamMember.objects.filter(
                is_active=True,
                role=TeamMember.Role.CO_DIRECTOR,
            ).order_by('sort_order', 'id')[:2]
        )
        if 'consultation_form' not in ctx:
            ctx['consultation_form'] = ConsultationForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = ConsultationForm(request.POST)
        if form.is_valid():
            req = form.save()
            ok = notify_admins_new_consultation(req)
            if ok:
                req.sms_sent = True
                req.save(update_fields=['sms_sent'])
            messages.success(
                request,
                'درخواست شما با موفقیت ثبت شد. به‌زودی با شما تماس می‌گیریم.',
            )
            return redirect(request.path + '#contact')
        ctx = self.get_context_data(consultation_form=form)
        messages.error(request, 'لطفاً فرم را به‌درستی تکمیل کنید.')
        return self.render_to_response(ctx)


class AboutView(TemplateView):
    def get_template_names(self):
        if _lang_is_en():
            return ['core/about_en.html']
        return ['core/about.html']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dept_managers'] = (
            TeamMember.objects.filter(
                is_active=True,
                role=TeamMember.Role.DEPT_MANAGER,
            ).order_by('sort_order', 'id')
        )
        ctx['directors'] = (
            TeamMember.objects.filter(
                is_active=True,
                role=TeamMember.Role.CO_DIRECTOR,
            ).order_by('sort_order', 'id')[:2]
        )
        return ctx
