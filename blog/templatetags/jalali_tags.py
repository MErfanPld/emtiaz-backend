from django import template
from django.utils import timezone

register = template.Library()

_MONTHS_FA = (
    '', 'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
)


@register.filter(name='jalali')
def jalali(value, fmt='j F Y'):
    """تبدیل تاریخ میلادی به جلالی.

    فرمت‌های رایج:
      j F Y  → ۱۵ مهر ۱۴۰۳
      Y/m/d  → ۱۴۰۳/۰۷/۱۵
    """
    if not value:
        return '—'
    try:
        import jdatetime
    except ImportError:
        return value.strftime('%Y-%m-%d') if hasattr(value, 'strftime') else str(value)

    if timezone.is_aware(value):
        value = timezone.localtime(value)
    jdt = jdatetime.datetime.fromgregorian(datetime=value)

    # جایگزینی توکن‌های ساده
    out = fmt
    out = out.replace('Y', str(jdt.year))
    out = out.replace('m', f'{jdt.month:02d}')
    out = out.replace('d', f'{jdt.day:02d}')
    out = out.replace('j', str(jdt.day))
    out = out.replace('F', _MONTHS_FA[jdt.month])
    out = out.replace('H', f'{jdt.hour:02d}')
    out = out.replace('i', f'{jdt.minute:02d}')
    return out
