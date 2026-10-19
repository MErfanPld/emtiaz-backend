from django.utils.translation import get_language
from django.views.generic import TemplateView

from real_estate.models import Property


def _lang_is_en():
    return (get_language() or 'fa')[:2] == 'en'


class HomeView(TemplateView):
    """صفحه اصلی — FA: home.html | EN: home_en.html"""

    def get_template_names(self):
        if _lang_is_en():
            return ['core/home_en.html']
        return ['core/home.html']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        featured = (
            Property.objects.filter(is_active=True)
            .order_by('-is_featured', '-created_at')[:8]
        )
        ctx['featured_properties'] = featured
        ctx['property_count'] = Property.objects.filter(is_active=True).count()
        return ctx


class AboutView(TemplateView):
    """معرفی مجموعه — FA: about.html | EN: about_en.html"""

    def get_template_names(self):
        if _lang_is_en():
            return ['core/about_en.html']
        return ['core/about.html']
