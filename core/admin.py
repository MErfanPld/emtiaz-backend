from django.contrib import admin

from .models import ConsultationRequest


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'request_type', 'status', 'sms_sent', 'created_at')
    list_filter = ('status', 'request_type', 'sms_sent')
    search_fields = ('full_name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'sms_sent')
