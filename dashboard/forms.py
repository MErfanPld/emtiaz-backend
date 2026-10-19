from django import forms
from django.forms import inlineformset_factory

from real_estate.models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # فقط فیلدهایی که در property_form.html رندر می‌شوند.
        # فیلدهای required مدل (مثل sort_order/image_count) اگر در POST نباشند
        # فرم را invalid می‌کنند و ثبت ملک fail می‌شود.
        fields = [
            'code', 'title', 'title_en', 'slug',
            'transaction_type', 'property_type',
            'area_name', 'area_name_en', 'address_line', 'address_line_en',
            'area_sqm', 'bedrooms', 'parking', 'floor',
            'year_built',
            'price', 'price_label', 'price_label_en',
            'cover_image', 'cover_image_url',
            'has_deed', 'is_complex_office',
            'is_active', 'is_featured', 'is_exclusive',
            'description', 'description_en',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'description_en': forms.Textarea(attrs={'rows': 4}),
            'code': forms.TextInput(attrs={'placeholder': 'مثلاً D-408'}),
            'price': forms.NumberInput(attrs={'min': 0}),
            'slug': forms.TextInput(attrs={'placeholder': 'خالی بگذارید تا خودکار ساخته شود'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اسلاگ اختیاری — در مدل save پر می‌شود
        self.fields['slug'].required = False
        for name, field in self.fields.items():
            css = (
                'w-full border border-[#c1c8c4] rounded-lg px-3 py-2 text-sm '
                'bg-white focus:outline-none focus:border-primary'
            )
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'rounded text-primary'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'text-sm'
            else:
                field.widget.attrs['class'] = css


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'image_url', 'caption', 'caption_en', 'sort_order']
        widgets = {
            'image_url': forms.URLInput(attrs={
                'class': 'w-full border border-[#c1c8c4] rounded-lg px-3 py-2 text-sm',
                'placeholder': 'https://...',
            }),
            'caption': forms.TextInput(attrs={
                'class': 'w-full border border-[#c1c8c4] rounded-lg px-2 py-1.5 text-sm',
            }),
            'caption_en': forms.TextInput(attrs={
                'class': 'w-full border border-[#c1c8c4] rounded-lg px-2 py-1.5 text-sm',
            }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'w-20 border border-[#c1c8c4] rounded-lg px-2 py-1.5 text-sm',
                'min': 0,
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ردیف‌های خالی گالری نباید validation را بشکنند
        self.fields['sort_order'].required = False


PropertyImageFormSet = inlineformset_factory(
    Property,
    PropertyImage,
    form=PropertyImageForm,
    fk_name='listing',
    extra=3,
    can_delete=True,
    max_num=30,
)
