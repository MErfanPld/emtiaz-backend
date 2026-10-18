from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """مدیر با شناسه اصلی شماره موبایل."""

    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_('شماره موبایل الزامی است.'))
        phone_number = self.normalize_phone(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    @staticmethod
    def normalize_phone(phone):
        phone = (phone or '').strip().replace(' ', '').replace('-', '')
        trans = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
        phone = phone.translate(trans)
        if phone.startswith('+98'):
            phone = '0' + phone[3:]
        if phone.startswith('98') and len(phone) >= 12:
            phone = '0' + phone[2:]
        return phone

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('approval_status', User.ApprovalStatus.PENDING)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('approval_status', User.ApprovalStatus.APPROVED)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('سوپریوزر باید is_staff=True داشته باشد.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('سوپریوزر باید is_superuser=True داشته باشد.'))

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """
    کاربر سفارشی املاک امتیاز.
    ورود با شماره موبایل؛ وضعیت تأیید جدا از is_active.
    """

    class ApprovalStatus(models.TextChoices):
        PENDING = 'pending', _('در انتظار تأیید')
        APPROVED = 'approved', _('تأیید شده')
        REJECTED = 'rejected', _('رد شده')

    username = None

    first_name = models.CharField(_('نام'), max_length=150, blank=True)
    last_name = models.CharField(_('نام خانوادگی'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('دسترسی به پنل ادمین'),
        default=False,
        help_text=_('تعیین می‌کند کاربر بتواند وارد پنل مدیریت جنگو شود.'),
    )
    is_active = models.BooleanField(
        _('فعال'),
        default=True,
        help_text=_('به‌جای حذف حساب، آن را غیرفعال کنید.'),
    )
    is_superuser = models.BooleanField(
        _('مدیر کل'),
        default=False,
        help_text=_('تمام مجوزها را بدون محدودیت دارد.'),
    )
    last_login = models.DateTimeField(_('آخرین ورود'), blank=True, null=True)
    date_joined = models.DateTimeField(_('تاریخ عضویت'), auto_now_add=True)

    phone_number = models.CharField(
        _('شماره موبایل'),
        max_length=15,
        unique=True,
        help_text=_('مثال: 09123456789'),
    )

    email = models.EmailField(_('ایمیل'), blank=True, default='')

    personnel_code = models.CharField(
        _('کد پرسنلی'),
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    job_title = models.CharField(
        _('عنوان شغلی'),
        max_length=100,
        blank=True,
        default='',
    )

    branch = models.CharField(
        _('شعبه / واحد'),
        max_length=100,
        blank=True,
        default='',
    )

    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name=_('مدیر مستقیم'),
    )

    internal_notes = models.TextField(
        _('یادداشت داخلی'),
        blank=True,
        default='',
        help_text=_('فقط برای مدیران قابل مشاهده است.'),
    )

    approval_status = models.CharField(
        _('وضعیت تأیید'),
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
        db_index=True,
    )

    requested_at = models.DateTimeField(_('تاریخ درخواست'), auto_now_add=True)

    approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users',
        verbose_name=_('تأییدکننده'),
    )

    approved_at = models.DateTimeField(
        _('تاریخ تأیید / رد'),
        null=True,
        blank=True,
    )

    rejection_reason = models.TextField(_('دلیل رد'), blank=True, default='')

    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('آخرین ویرایش'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['approval_status', 'is_active']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else (self.phone_number or str(self.pk))

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = UserManager.normalize_phone(self.phone_number)
        super().save(*args, **kwargs)

    @property
    def is_approved(self):
        return self.approval_status == self.ApprovalStatus.APPROVED

    def can_authenticate(self):
        return self.is_active and self.is_approved

    def approve(self, by_user, commit=True):
        from django.utils import timezone
        self.approval_status = self.ApprovalStatus.APPROVED
        self.approved_by = by_user
        self.approved_at = timezone.now()
        self.rejection_reason = ''
        if commit:
            self.save(update_fields=[
                'approval_status', 'approved_by', 'approved_at',
                'rejection_reason', 'updated_at',
            ])

    def reject(self, by_user, reason='', commit=True):
        from django.utils import timezone
        self.approval_status = self.ApprovalStatus.REJECTED
        self.approved_by = by_user
        self.approved_at = timezone.now()
        self.rejection_reason = reason
        if commit:
            self.save(update_fields=[
                'approval_status', 'approved_by', 'approved_at',
                'rejection_reason', 'updated_at',
            ])
