from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom manager for User model that supports email and phone as identifiers."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('approval_status', User.ApprovalStatus.PENDING)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('approval_status', User.ApprovalStatus.APPROVED)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model for Emtiaz Real Estate platform.
    - Uses email as the primary unique identifier for authentication.
    - Separates account activation (is_active) from managerial approval (approval_status).
    - Supports organizational fields needed by a real-estate agency.
    """

    class ApprovalStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')

    # Override username to be optional / not primary
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )

    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        help_text=_('Iranian mobile number, e.g. 09123456789'),
    )

    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/%Y/%m/',
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        _('date of birth'),
        null=True,
        blank=True,
    )

    # Organizational
    personnel_code = models.CharField(
        _('personnel code'),
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    job_title = models.CharField(
        _('job title'),
        max_length=100,
        blank=True,
        default='',
    )

    branch = models.CharField(
        _('branch / unit'),
        max_length=100,
        blank=True,
        default='',
        help_text=_('Organizational branch or unit'),
    )

    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name=_('direct manager'),
    )

    internal_notes = models.TextField(
        _('internal notes'),
        blank=True,
        default='',
        help_text=_('Internal management notes (not visible to the user)'),
    )

    # Approval workflow (separated from is_active)
    approval_status = models.CharField(
        _('approval status'),
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
        db_index=True,
    )

    requested_at = models.DateTimeField(
        _('requested at'),
        auto_now_add=True,
    )

    approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users',
        verbose_name=_('approved by'),
    )

    approved_at = models.DateTimeField(
        _('approved / rejected at'),
        null=True,
        blank=True,
    )

    rejection_reason = models.TextField(
        _('rejection reason'),
        blank=True,
        default='',
    )

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # for createsuperuser

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['approval_status', 'is_active']),
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.email

    @property
    def is_approved(self):
        """Return True only when the account has been managerially approved."""
        return self.approval_status == self.ApprovalStatus.APPROVED

    def can_authenticate(self):
        """
        Business rule: a user can obtain / use protected resources only when
        the account is both active and approved.
        """
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
                'rejection_reason', 'updated_at'
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
                'rejection_reason', 'updated_at'
            ])
