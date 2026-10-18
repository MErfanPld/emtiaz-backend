from django.utils.translation import get_language
from django.views.generic import TemplateView


def _lang_is_en():
    return (get_language() or 'fa')[:2] == 'en'


class HomeView(TemplateView):
    """صفحه اصلی — FA: home.html | EN: home_en.html"""

    def get_template_names(self):
        if _lang_is_en():
            return ['core/home_en.html']
        return ['core/home.html']


class AboutView(TemplateView):
    """معرفی مجتمع — FA: about.html | EN: about_en.html"""

    def get_template_names(self):
        if _lang_is_en():
            return ['core/about_en.html']
        return ['core/about.html']
