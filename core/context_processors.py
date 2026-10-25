"""Context processors for site-wide template variables."""

from core.models import ConsultationRequest
from real_estate.models import Property


def dashboard_notifications(request):
    """تعداد اعلان‌های خوانده‌نشده برای badge چشمک‌زن سایدبار."""
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {}
    if not getattr(request.user, 'is_approved', False):
        return {}

    pending_props = Property.objects.filter(
        publish_status=Property.PublishStatus.PENDING
    ).count()
    new_consults = ConsultationRequest.objects.filter(
        status=ConsultationRequest.Status.NEW
    ).count()
    total = pending_props + new_consults

    return {
        'notif_pending_properties': pending_props,
        'notif_new_consultations': new_consults,
        'notif_total': total,
        'has_notifications': total > 0,
    }
