from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import (
    CustomPasswordChangeForm,
    EmailAuthenticationForm,
    ProfileForm,
    RegisterForm,
)
from .models import User


class ApprovedRequiredMixin:
    """Mixin: user must be authenticated, active and approved."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_active:
            messages.error(request, 'حساب شما غیرفعال است.')
            logout(request)
            return redirect('accounts:login')
        if not request.user.is_approved:
            return redirect('accounts:pending')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember = form.cleaned_data.get('remember_me')
        if not remember:
            self.request.session.set_expiry(0)  # browser session
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 14)  # 14 days
        return super().form_valid(form)

    def get_success_url(self):
        # Prefer next param, then dashboard, then home
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        try:
            return reverse_lazy('dashboard:index')
        except Exception:
            return reverse_lazy('core:home')


class CustomLogoutView(LogoutView):
    """Logout only via POST (CSRF protected by Django)."""
    next_page = reverse_lazy('accounts:login')
    http_method_names = ['post', 'options']


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:register_done')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'ثبت‌نام با موفقیت انجام شد. حساب شما پس از تأیید مدیر فعال خواهد شد.'
        )
        return response


class RegisterDoneView(TemplateView):
    template_name = 'accounts/register_done.html'


class PendingView(TemplateView):
    """Shown when user is logged-in but not yet approved / rejected."""
    template_name = 'accounts/pending.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.is_approved and request.user.is_active:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProfileView(ApprovedRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'پروفایل با موفقیت به‌روزرسانی شد.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(ApprovedRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, 'رمز عبور با موفقیت تغییر کرد.')
        return super().form_valid(form)
