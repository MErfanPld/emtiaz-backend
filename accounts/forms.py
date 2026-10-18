from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

INPUT_CLASS = (
    'w-full px-4 py-3 rounded-lg border border-outline-variant bg-surface-container-lowest '
    'text-sm text-on-surface focus:outline-none focus:border-primary focus:ring-1 focus:ring-secondary/40'
)


class PhoneAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_('شماره موبایل'),
        widget=forms.TextInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm text-brand-charcoal transition duration-150',
            'placeholder': '09123456789',
            'autocomplete': 'tel',
            'dir': 'ltr',
            'id': 'username',
            'inputmode': 'tel',
        }),
    )
    password = forms.CharField(
        label=_('رمز عبور'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm text-brand-charcoal transition duration-150 tracking-wider',
            'placeholder': 'رمز عبور خود را وارد کنید',
            'autocomplete': 'current-password',
            'id': 'password',
        }),
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label=_('مرا به خاطر بسپار'),
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary',
            'id': 'id_remember_me',
        }),
    )

    error_messages = {
        'invalid_login': _('شماره موبایل یا رمز عبور صحیح نیست.'),
        'inactive': _('این حساب غیرفعال است.'),
    }

    def clean_username(self):
        return User.objects.normalize_phone(self.cleaned_data.get('username', ''))

    def clean(self):
        phone = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if phone and password:
            self.user_cache = authenticate(self.request, username=phone, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            if not getattr(self.user_cache, 'is_approved', False):
                if self.user_cache.approval_status == User.ApprovalStatus.PENDING:
                    raise forms.ValidationError(
                        _('حساب شما در انتظار تأیید مدیر است. پس از تأیید می‌توانید وارد شوید.'),
                        code='pending',
                    )
                if self.user_cache.approval_status == User.ApprovalStatus.REJECTED:
                    raise forms.ValidationError(
                        _('درخواست عضویت شما رد شده است. با مدیریت تماس بگیرید.'),
                        code='rejected',
                    )
                raise forms.ValidationError(_('حساب شما تأیید نشده است.'), code='not_approved')
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
            'placeholder': 'رمز عبور',
            'autocomplete': 'new-password',
        }),
        strip=False,
    )
    password2 = forms.CharField(
        label=_('تکرار رمز عبور'),
        widget=forms.PasswordInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
            'placeholder': 'تکرار رمز عبور',
            'autocomplete': 'new-password',
        }),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'job_title')
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': '09123456789', 'dir': 'ltr', 'inputmode': 'tel',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': 'نام',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': 'نام خانوادگی',
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': 'عنوان شغلی',
            }),
        }
        labels = {
            'phone_number': _('شماره موبایل'),
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'job_title': _('عنوان شغلی'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('phone_number', 'first_name', 'last_name', 'job_title'):
            self.fields[name].required = True

    def clean_phone_number(self):
        phone = User.objects.normalize_phone(self.cleaned_data.get('phone_number', ''))
        if not phone:
            raise forms.ValidationError(_('شماره موبایل الزامی است.'))
        if not (phone.startswith('09') and len(phone) == 11 and phone.isdigit()):
            raise forms.ValidationError(_('شماره موبایل معتبر نیست. مثال: 09123456789'))
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(_('این شماره موبایل قبلاً ثبت شده است.'))
        return phone

    def clean_first_name(self):
        value = (self.cleaned_data.get('first_name') or '').strip()
        if not value:
            raise forms.ValidationError(_('نام الزامی است.'))
        return value

    def clean_last_name(self):
        value = (self.cleaned_data.get('last_name') or '').strip()
        if not value:
            raise forms.ValidationError(_('نام خانوادگی الزامی است.'))
        return value

    def clean_job_title(self):
        value = (self.cleaned_data.get('job_title') or '').strip()
        if not value:
            raise forms.ValidationError(_('عنوان شغلی الزامی است.'))
        return value

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') and cleaned.get('password2') and cleaned['password1'] != cleaned['password2']:
            self.add_error('password2', _('رمزهای عبور یکسان نیستند.'))
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.approval_status = User.ApprovalStatus.PENDING
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'job_title')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'dir': 'ltr'}),
            'job_title': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'email': _('ایمیل'),
            'job_title': _('عنوان شغلی'),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            'old_password': _('رمز عبور فعلی'),
            'new_password1': _('رمز عبور جدید'),
            'new_password2': _('تکرار رمز عبور جدید'),
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': INPUT_CLASS})
            if name in labels:
                field.label = labels[name]


class PasswordResetRequestForm(forms.Form):
    phone_number = forms.CharField(
        label=_('شماره موبایل'),
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
            'placeholder': '09123456789', 'dir': 'ltr', 'inputmode': 'tel',
        }),
    )

    def clean_phone_number(self):
        phone = User.objects.normalize_phone(self.cleaned_data.get('phone_number', ''))
        if not (phone.startswith('09') and len(phone) == 11 and phone.isdigit()):
            raise forms.ValidationError(_('شماره موبایل معتبر نیست.'))
        if not User.objects.filter(phone_number=phone, is_active=True).exists():
            raise forms.ValidationError(_('اگر این شماره ثبت شده باشد، کد ارسال می‌شود.'))
        return phone


class PasswordResetConfirmForm(forms.Form):
    phone_number = forms.CharField(
        label=_('شماره موبایل'), max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
            'placeholder': '09123456789', 'dir': 'ltr', 'inputmode': 'tel',
        }),
    )
    code = forms.CharField(
        label=_('کد تأیید'), max_length=6, min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm tracking-widest',
            'placeholder': '123456', 'dir': 'ltr', 'inputmode': 'numeric',
        }),
    )
    password1 = forms.CharField(
        label=_('رمز عبور جدید'), strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
            'placeholder': 'رمز عبور جدید', 'autocomplete': 'new-password',
        }),
    )
    password2 = forms.CharField(
        label=_('تکرار رمز عبور جدید'), strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
            'placeholder': 'تکرار رمز عبور جدید', 'autocomplete': 'new-password',
        }),
    )

    def clean_phone_number(self):
        return User.objects.normalize_phone(self.cleaned_data.get('phone_number', ''))

    def clean_code(self):
        return (self.cleaned_data.get('code') or '').strip()

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') and cleaned.get('password2') and cleaned['password1'] != cleaned['password2']:
            self.add_error('password2', _('رمزهای عبور یکسان نیستند.'))
        return cleaned
