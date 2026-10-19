"""فیلترهای اعداد و تاریخ فارسی."""
from django import template
from django.utils import timezone
from django.utils.translation import get_language

register = template.Library()

_FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
_MONTHS_FA = (
    '', 'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
)


def to_persian_digits(value):
    if value is None:
        return ''
    return str(value).translate(_FA_DIGITS)


@register.filter(name='fa_num')
def fa_num(value):
    """تبدیل ارقام لاتین به فارسی — فقط وقتی زبان fa است."""
    if value is None:
        return ''
    text = str(value)
    if (get_language() or 'fa')[:2] == 'en':
        return text
    return text.translate(_FA_DIGITS)


@register.filter(name='jalali')
def jalali(value, fmt='j F Y'):
    """تاریخ جلالی با ارقام فارسی.

    j F Y → ۱۵ مهر ۱۴۰۳
    Y/m/d → ۱۴۰۳/۰۷/۱۵
    """
    if not value:
        return '—'
    try:
        import jdatetime
    except ImportError:
        s = value.strftime('%Y-%m-%d') if hasattr(value, 'strftime') else str(value)
        return to_persian_digits(s) if (get_language() or 'fa')[:2] != 'en' else s

    if timezone.is_aware(value):
        value = timezone.localtime(value)
    jdt = jdatetime.datetime.fromgregorian(datetime=value)

    out = fmt
    out = out.replace('Y', str(jdt.year))
    out = out.replace('m', f'{jdt.month:02d}')
    out = out.replace('d', f'{jdt.day:02d}')
    out = out.replace('j', str(jdt.day))
    out = out.replace('F', _MONTHS_FA[jdt.month])
    out = out.replace('H', f'{jdt.hour:02d}')
    out = out.replace('i', f'{jdt.minute:02d}')

    if (get_language() or 'fa')[:2] != 'en':
        out = to_persian_digits(out)
    return out
