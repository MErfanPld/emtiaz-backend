import logging
import random

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import (
    CustomPasswordChangeForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
    PhoneAuthenticationForm,
    ProfileForm,
    RegisterForm,
)
from .models import User

logger = logging.getLogger(__name__)

OTP_CACHE_PREFIX = 'pwd_reset_otp_'
OTP_TTL_SECONDS = 300  # 5 دقیقه


class ApprovedRequiredMixin:
    """کاربر باید وارد شده، فعال و تأییدشده باشد."""

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
    authentication_form = PhoneAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        # اول لاگین، بعد تنظیم انقضای سشن (مرا به خاطر بسپار)
        response = super().form_valid(form)
        remember = form.cleaned_data.get('remember_me')
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 14)  # ۱۴ روز
        else:
            self.request.session.set_expiry(0)  # تا بستن مرورگر
        self.request.session.modified = True
        return response

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        try:
            return str(reverse_lazy('dashboard:index'))
        except Exception:
            return str(reverse_lazy('core:home'))


class CustomLogoutView(LogoutView):
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


def _send_sms_otp_test(phone: str, code: str) -> None:
    """
    ارسال تستی SMS.
    فعلاً فقط لاگ و پیام کنسول — بعداً به پنل واقعی وصل می‌شود.
    """
    msg = f'[SMS TEST] to={phone} code={code}'
    logger.info(msg)
    print(msg)  # noqa: T201 — حالت توسعه


class PasswordResetRequestView(View):
    template_name = 'accounts/password_reset_request.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return render(request, self.template_name, {'form': PasswordResetRequestForm()})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        phone = form.cleaned_data['phone_number']
        code = f'{random.randint(100000, 999999)}'
        cache.set(f'{OTP_CACHE_PREFIX}{phone}', code, OTP_TTL_SECONDS)
        _send_sms_otp_test(phone, code)

        # در حالت تست کد را در پیام نشان می‌دهیم
        messages.success(
            request,
            f'کد تأیید ارسال شد. (حالت تست: {code}) — اعتبار ۵ دقیقه',
        )
        return redirect('accounts:password_reset_confirm')


class PasswordResetConfirmView(View):
    template_name = 'accounts/password_reset_confirm.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return render(request, self.template_name, {'form': PasswordResetConfirmForm()})

    def post(self, request):
        form = PasswordResetConfirmForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        phone = form.cleaned_data['phone_number']
        code = form.cleaned_data['code']
        expected = cache.get(f'{OTP_CACHE_PREFIX}{phone}')

        if not expected or str(expected) != str(code):
            form.add_error('code', 'کد تأیید نامعتبر یا منقضی شده است.')
            return render(request, self.template_name, {'form': form})

        try:
            user = User.objects.get(phone_number=phone, is_active=True)
        except User.DoesNotExist:
            form.add_error('phone_number', 'کاربری با این شماره یافت نشد.')
            return render(request, self.template_name, {'form': form})

        user.set_password(form.cleaned_data['password1'])
        user.save(update_fields=['password'])
        cache.delete(f'{OTP_CACHE_PREFIX}{phone}')

        messages.success(request, 'رمز عبور با موفقیت تغییر کرد. اکنون وارد شوید.')
        return redirect('accounts:login')
