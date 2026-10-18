from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('-created_at',)
    list_display = (
        'email', 'get_full_name', 'phone_number', 'approval_status_badge',
        'is_active', 'is_staff', 'job_title', 'created_at',
    )
    list_filter = (
        'approval_status', 'is_active', 'is_staff', 'is_superuser',
        'groups', 'created_at',
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'personnel_code')
    readonly_fields = (
        'requested_at', 'approved_at', 'last_login', 'date_joined',
        'created_at', 'updated_at',
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'phone_number', 'avatar',
                'date_of_birth', 'username',
            )
        }),
        (_('Organizational'), {
            'fields': (
                'personnel_code', 'job_title', 'branch', 'manager', 'internal_notes',
            )
        }),
        (_('Approval'), {
            'fields': (
                'approval_status', 'requested_at', 'approved_by',
                'approved_at', 'rejection_reason',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'phone_number',
                'password1', 'password2', 'is_staff', 'is_superuser',
                'approval_status',
            ),
        }),
    )

    actions = ['approve_selected', 'reject_selected', 'activate_selected', 'deactivate_selected']

    @admin.display(description=_('Approval'), ordering='approval_status')
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

    @admin.action(description=_('Approve selected users'))
    def approve_selected(self, request, queryset):
        for user in queryset.exclude(approval_status=User.ApprovalStatus.APPROVED):
            user.approve(by_user=request.user)
        self.message_user(request, _('Selected users have been approved.'))

    @admin.action(description=_('Reject selected users'))
    def reject_selected(self, request, queryset):
        for user in queryset.exclude(approval_status=User.ApprovalStatus.REJECTED):
            user.reject(by_user=request.user, reason='Rejected via admin action')
        self.message_user(request, _('Selected users have been rejected.'))

    @admin.action(description=_('Activate selected users'))
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _('Selected users have been activated.'))

    @admin.action(description=_('Deactivate selected users'))
    def deactivate_selected(self, request, queryset):
        queryset.exclude(pk=request.user.pk).update(is_active=False)
        self.message_user(request, _('Selected users have been deactivated.'))
