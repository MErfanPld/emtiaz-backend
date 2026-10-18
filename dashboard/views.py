from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


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
