from django.db.models import Prefetch, Q
from django.utils.translation import get_language
from django.views.generic import DetailView, ListView

from .models import Property, PropertyImage


def _lang_is_en():
    return (get_language() or 'fa')[:2] == 'en'


class PropertyListView(ListView):
    model = Property
    context_object_name = 'properties'
    paginate_by = 12

    def get_template_names(self):
        if _lang_is_en():
            return ['real_estate/property_list_en.html']
        return ['real_estate/property_list.html']

    def get_queryset(self):
        qs = Property.objects.filter(is_active=True)
        tx = self.request.GET.get('tx')
        ptype = self.request.GET.get('type')
        area = self.request.GET.get('area')
        sort = self.request.GET.get('sort', 'newest')

        if tx in dict(Property.TransactionType.choices):
            qs = qs.filter(transaction_type=tx)
        if ptype in dict(Property.PropertyType.choices):
            qs = qs.filter(property_type=ptype)
        if area:
            qs = qs.filter(
                Q(area_name__icontains=area) | Q(area_name_en__icontains=area)
            )

        if sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'area_desc':
            qs = qs.order_by('-area_sqm')
        elif sort == 'exclusive':
            qs = qs.filter(is_exclusive=True).order_by('-created_at')
        else:
            qs = qs.order_by('-is_featured', '-created_at')

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_count'] = Property.objects.filter(is_active=True).count()
        ctx['current_tx'] = self.request.GET.get('tx', '')
        ctx['current_type'] = self.request.GET.get('type', '')
        ctx['current_area'] = self.request.GET.get('area', '')
        ctx['current_sort'] = self.request.GET.get('sort', 'newest')
        ctx['transaction_types'] = Property.TransactionType.choices
        ctx['property_types'] = Property.PropertyType.choices
        return ctx


class PropertyDetailView(DetailView):
    model = Property
    context_object_name = 'property'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Property.objects.filter(is_active=True).prefetch_related(
            Prefetch('images', queryset=PropertyImage.objects.order_by('sort_order', 'id'))
        )

    def get_template_names(self):
        if _lang_is_en():
            return ['real_estate/property_detail_en.html']
        return ['real_estate/property_detail.html']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.object
        ctx['gallery'] = obj.gallery_urls()
        ctx['gallery_count'] = obj.gallery_count()
        ctx['similar'] = (
            Property.objects.filter(is_active=True)
            .filter(Q(area_name=obj.area_name) | Q(property_type=obj.property_type))
            .exclude(pk=obj.pk)[:3]
        )
        return ctx
