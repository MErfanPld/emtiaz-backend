"""سازگاری با تمپلیت‌های قبلی — از core.persian استفاده کنید."""
from core.templatetags.persian import fa_num, jalali  # noqa: F401
from django import template

register = template.Library()
register.filter('jalali', jalali)
register.filter('fa_num', fa_num)
