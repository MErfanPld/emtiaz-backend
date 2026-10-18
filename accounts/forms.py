from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class EmailAuthenticationForm(AuthenticationForm):
    """Login form using email as username field."""

    username = forms.EmailField(
        label=_('ایمیل'),
        widget=forms.EmailInput(attrs={
            'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm text-brand-charcoal transition duration-150',
            'placeholder': 'ایمیل خود را وارد کنید',
            'autocomplete': 'email',
            'dir': 'ltr',
            'id': 'username',
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
        label=_('مرا به خاطر بسپار'),
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-checkbox w-4 h-4 rounded border-gray-300 text-primary',
            'id': 'remember',
        }),
    )

    error_messages = {
        'invalid_login': _('ایمیل یا رمز عبور صحیح نیست.'),
        'inactive': _('این حساب غیرفعال است.'),
    }

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            # Extra business rule: must be approved
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
                raise forms.ValidationError(
                    _('حساب شما تأیید نشده است.'),
                    code='not_approved',
                )
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    """Public registration – always creates pending account."""

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
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'job_title')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': 'ایمیل',
                'dir': 'ltr',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': 'نام',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': 'نام خانوادگی',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': '۰۹۱۲۳۴۵۶۷۸۹',
                'dir': 'ltr',
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
                'placeholder': 'عنوان شغلی (اختیاری)',
            }),
        }
        labels = {
            'email': _('ایمیل'),
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'phone_number': _('شماره موبایل'),
            'job_title': _('عنوان شغلی'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('کاربری با این ایمیل قبلاً ثبت‌نام کرده است.'))
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(_('این شماره موبایل قبلاً ثبت شده است.'))
        return phone

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
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
    """User can edit limited profile fields only."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'job_title', 'avatar', 'date_of_birth')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm'}),
            'phone_number': forms.TextInput(attrs={'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm', 'dir': 'ltr'}),
            'job_title': forms.TextInput(attrs={'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm', 'type': 'date'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'text-sm'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm',
            })
