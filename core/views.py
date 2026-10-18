from django.utils.translation import get_language
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    صفحه اصلی سایت عمومی.
    FA: core/home.html  |  EN: core/home_en.html
    """

    def get_template_names(self):
        lang = (get_language() or 'fa')[:2]
        if lang == 'en':
            return ['core/home_en.html']
        return ['core/home.html']
