from django.utils.translation import get_language
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    صفحه اصلی سایت عمومی.
    فعلاً محتوای مارکتینگ استاتیک است (SEO خوب).
    بعداً بخش‌های املاک/مقالات/دفاتر از دیتابیس تزریق می‌شود.
    تمپلیت انگلیسی جدا: core/home_en.html
    """

    def get_template_names(self):
        if get_language() == 'en':
            return ['core/home_en.html']
        return ['core/home.html']
