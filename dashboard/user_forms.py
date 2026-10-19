from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

INPUT_CSS = 'w-full border border-[#c1c8c4] rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-1 focus:ring-primary'


class DashboardUserForm(forms.ModelForm):
    """ویرایش کاربر از پنل داشبورد — بدون ارتقای خودسرانه توسط غیر سوپریوزر."""

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().order_by('name'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='گروه‌ها',
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type').order_by(
            'content_type__app_label', 'codename'
        ),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='مجوزهای مستقیم',
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': INPUT_CSS, 'autocomplete': 'new-password'}),
        label='رمز عبور جدید',
        help_text='خالی بگذارید تا تغییر نکند.',
    )

    class Meta:
        model = User
        fields = [
            'phone_number', 'first_name', 'last_name', 'email',
            'job_title', 'branch', 'personnel_code',
            'approval_status', 'rejection_reason', 'internal_notes',
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions',
        ]

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ('groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser'):
                continue
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = INPUT_CSS + ' min-h-[80px]'
                field.widget.attrs['rows'] = 3
            else:
                field.widget.attrs['class'] = INPUT_CSS

        # فقط سوپریوزر می‌تواند is_superuser / user_permissions را ببیند
        if not (self.request_user and self.request_user.is_superuser):
            self.fields.pop('is_superuser', None)
            self.fields.pop('user_permissions', None)
            # staff معمولی نمی‌تواند staff دیگر را staff کند مگر سوپر
            if self.instance and self.instance.is_superuser:
                self.fields['is_staff'].disabled = True

    def clean_phone_number(self):
        phone = User.objects.normalize_phone(self.cleaned_data['phone_number'])
        qs = User.objects.filter(phone_number=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('new_password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
            self.save_m2m()
        return user


class DashboardUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': INPUT_CSS}),
    )
    password2 = forms.CharField(
        label='تکرار رمز',
        widget=forms.PasswordInput(attrs={'class': INPUT_CSS}),
    )

    class Meta:
        model = User
        fields = [
            'phone_number', 'first_name', 'last_name', 'email',
            'job_title', 'approval_status', 'is_active', 'is_staff',
        ]

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ('is_active', 'is_staff'):
                continue
            field.widget.attrs['class'] = INPUT_CSS

    def clean_phone_number(self):
        phone = User.objects.normalize_phone(self.cleaned_data['phone_number'])
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        return phone

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            self.add_error('password2', 'رمزها یکسان نیستند.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type').order_by(
            'content_type__app_label', 'codename'
        ),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='مجوزها',
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = INPUT_CSS
        self.fields['name'].label = 'نام گروه'
