from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('-created_at',)
    list_display = (
        'phone_number', 'get_full_name', 'email', 'approval_status_badge',
        'is_active', 'is_staff', 'job_title', 'created_at',
    )
    list_filter = (
        'approval_status', 'is_active', 'is_staff', 'is_superuser',
        'groups', 'created_at',
    )
    search_fields = ('phone_number', 'email', 'first_name', 'last_name', 'personnel_code')
    readonly_fields = (
        'requested_at', 'approved_at', 'last_login', 'date_joined',
        'created_at', 'updated_at',
    )

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('اطلاعات شخصی'), {
            'fields': (
                'first_name', 'last_name', 'email', 'avatar',
                'date_of_birth', 'username',
            )
        }),
        (_('سازمانی'), {
            'fields': (
                'personnel_code', 'job_title', 'branch', 'manager', 'internal_notes',
            )
        }),
        (_('تأیید'), {
            'fields': (
                'approval_status', 'requested_at', 'approved_by',
                'approved_at', 'rejection_reason',
            )
        }),
        (_('دسترسی‌ها'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
            )
        }),
        (_('تاریخ‌ها'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 'first_name', 'last_name', 'email',
                'password1', 'password2', 'is_staff', 'is_superuser',
                'approval_status',
            ),
        }),
    )

    actions = ['approve_selected', 'reject_selected', 'activate_selected', 'deactivate_selected']

    @admin.display(description=_('وضعیت تأیید'), ordering='approval_status')
    def approval_status_badge(self, obj):
        colors = {
            'pending': '#f0ad4e',
            'approved': '#5cb85c',
            'rejected': '#d9534f',
        }
        color = colors.get(obj.approval_status, '#777')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;">{}</span>',
            color,
            obj.get_approval_status_display(),
        )

    @admin.action(description=_('تأیید کاربران انتخاب‌شده'))
    def approve_selected(self, request, queryset):
        for user in queryset.exclude(approval_status=User.ApprovalStatus.APPROVED):
            user.approve(by_user=request.user)
        self.message_user(request, _('کاربران انتخاب‌شده تأیید شدند.'))

    @admin.action(description=_('رد کاربران انتخاب‌شده'))
    def reject_selected(self, request, queryset):
        for user in queryset.exclude(approval_status=User.ApprovalStatus.REJECTED):
            user.reject(by_user=request.user, reason='رد از طریق پنل ادمین')
        self.message_user(request, _('کاربران انتخاب‌شده رد شدند.'))

    @admin.action(description=_('فعال‌سازی'))
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _('کاربران فعال شدند.'))

    @admin.action(description=_('غیرفعال‌سازی'))
    def deactivate_selected(self, request, queryset):
        queryset.exclude(pk=request.user.pk).update(is_active=False)
        self.message_user(request, _('کاربران غیرفعال شدند.'))
