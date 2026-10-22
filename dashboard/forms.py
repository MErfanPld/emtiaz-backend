from django import forms
from django.forms import inlineformset_factory

from real_estate.models import Property, PropertyImage

# نشان‌ها: مقدار فارسی → انگلیسی (همگام‌سازی خودکار در قالب)
BADGE_MAP = {
    '': '',
    'فروش انحصاری': 'Exclusive listing',
    'نوساز': 'Brand new',
    'سند تک‌برگ': 'Single-sheet deed',
    'موقعیت عالی': 'Prime location',
    'ویژه مجموعه': 'Complex exclusive',
    'پیش‌فروش': 'Pre-sale',
    'رهن کامل': 'Full deposit',
    'تخلیه فوری': 'Immediate delivery',
    'بازسازی‌شده': 'Renovated',
    'پارکینگ اختصاصی': 'Private parking',
}

BADGE_CHOICES = [('', '— بدون نشان —')] + [(k, k) for k in BADGE_MAP if k]

# برچسب قیمت: فارسی → انگلیسی
PRICE_LABEL_MAP = {
    '': '',
    'توافقی': 'Negotiable',
    'قیمت نهایی': 'Final price',
    'شروع از': 'Starting from',
    'متری': 'Per sqm',
    'ماهانه': 'Monthly',
    'رهن + اجاره': 'Deposit + rent',
}

PRICE_LABEL_CHOICES = [('', '— نمایش عدد قیمت —')] + [(k, k) for k in PRICE_LABEL_MAP if k]

AGENCY_FA_DEFAULT = 'مجموعه املاک امتیاز'
AGENCY_EN_DEFAULT = 'Emtiaz Real Estate Complex'

CSS_INPUT = (
    'w-full border border-[#c1c8c4] rounded-lg px-3 py-2 text-sm '
    'bg-white focus:outline-none focus:border-primary'
)


def _digits_only(value):
    """حذف جداکننده هزارگان و ارقام فارسی/عربی → عدد خام."""
    if value is None:
        return ''
    s = str(value).strip()
    trans = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
    s = s.translate(trans)
    s = s.replace(',', '').replace('٬', '').replace(' ', '').replace('_', '')
    return s


class PropertyForm(forms.ModelForm):
    badge_primary = forms.ChoiceField(
        label='نشان اصلی',
        choices=BADGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': CSS_INPUT, 'id': 'id_badge_primary'}),
    )
    badge_primary_en = forms.CharField(
        label='نشان اصلی (انگلیسی)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': CSS_INPUT,
            'id': 'id_badge_primary_en',
            'readonly': True,
            'placeholder': 'خودکار از نشان فارسی',
        }),
    )
    badge_secondary = forms.ChoiceField(
        label='نشان فرعی',
        choices=BADGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': CSS_INPUT, 'id': 'id_badge_secondary'}),
    )
    badge_secondary_en = forms.CharField(
        label='نشان فرعی (انگلیسی)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': CSS_INPUT,
            'id': 'id_badge_secondary_en',
            'readonly': True,
            'placeholder': 'خودکار از نشان فارسی',
        }),
    )
    price_label = forms.ChoiceField(
        label='برچسب قیمت',
        choices=PRICE_LABEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': CSS_INPUT, 'id': 'id_price_label'}),
        help_text='اگر انتخاب شود به‌جای عدد قیمت نمایش داده می‌شود.',
    )
    price_label_en = forms.CharField(
        label='برچسب قیمت (انگلیسی)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': CSS_INPUT,
            'id': 'id_price_label_en',
            'readonly': True,
            'placeholder': 'خودکار از برچسب فارسی',
        }),
    )
    price = forms.CharField(
        label='قیمت (تومان)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': CSS_INPUT,
            'id': 'id_price',
            'dir': 'ltr',
            'inputmode': 'numeric',
            'placeholder': 'مثلاً 45,000,000,000',
            'autocomplete': 'off',
        }),
        help_text='هر ۳ رقم با ویرگول جدا می‌شود.',
    )

    class Meta:
        model = Property
        fields = [
            'code', 'title', 'title_en', 'slug',
            'transaction_type', 'property_type',
            'area_name', 'area_name_en', 'address_line', 'address_line_en',
            'area_sqm', 'bedrooms', 'parking', 'floor', 'floor_en',
            'year_built', 'year_built_en',
            'price', 'price_label', 'price_label_en',
            'agency_name', 'agency_name_en',
            'consultant_name', 'consultant_name_en', 'consultant_phone',
            'badge_primary', 'badge_primary_en',
            'badge_secondary', 'badge_secondary_en',
            'cover_image', 'cover_image_url',
            'has_deed', 'is_complex_office', 'has_pool_or_roof', 'is_brand_builder',
            'is_active', 'is_featured', 'is_exclusive',
            'sort_order',
            'description', 'description_en',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'description_en': forms.Textarea(attrs={'rows': 4}),
            'code': forms.TextInput(attrs={'placeholder': 'مثلاً D-408'}),
            'slug': forms.TextInput(attrs={'placeholder': 'خالی بگذارید تا خودکار ساخته شود'}),
            'consultant_phone': forms.TextInput(attrs={'placeholder': '09xxxxxxxxx', 'dir': 'ltr'}),
            'sort_order': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        if 'sort_order' in self.fields:
            self.fields['sort_order'].required = False

        # پیش‌فرض‌ها فقط برای ساخت جدید (instance بدون pk)
        is_create = not (self.instance and self.instance.pk)
        if is_create:
            self.fields['agency_name'].initial = AGENCY_FA_DEFAULT
            self.fields['agency_name_en'].initial = AGENCY_EN_DEFAULT
            if user is not None:
                full = (user.get_full_name() or '').strip()
                if full:
                    self.fields['consultant_name'].initial = full
                    self.fields['consultant_name_en'].initial = full
                phone = getattr(user, 'phone_number', '') or ''
                if phone and not self.fields['consultant_phone'].initial:
                    self.fields['consultant_phone'].initial = phone

        # نمایش قیمت با جداکننده هنگام ویرایش
        if self.instance and self.instance.pk and self.instance.price:
            try:
                self.initial['price'] = f'{int(self.instance.price):,}'
            except (TypeError, ValueError):
                pass

        # اگر مقدار ذخیره‌شده در choices نباشد، اضافه کن تا select نشکند
        for field_name, choices in (
            ('badge_primary', BADGE_CHOICES),
            ('badge_secondary', BADGE_CHOICES),
            ('price_label', PRICE_LABEL_CHOICES),
        ):
            val = None
            if self.instance and self.instance.pk:
                val = getattr(self.instance, field_name, None) or ''
            if val and val not in dict(choices):
                self.fields[field_name].choices = list(choices) + [(val, val)]

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'rounded text-primary'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'text-sm'
            else:
                existing = field.widget.attrs.get('class', '')
                if 'w-full' not in existing:
                    field.widget.attrs['class'] = CSS_INPUT

    def clean_price(self):
        raw = _digits_only(self.cleaned_data.get('price') or '')
        if not raw:
            return 0
        try:
            return int(raw)
        except ValueError:
            raise forms.ValidationError('قیمت باید عدد معتبر باشد.')

    def clean_badge_primary_en(self):
        fa = self.cleaned_data.get('badge_primary') or ''
        en = (self.cleaned_data.get('badge_primary_en') or '').strip()
        return BADGE_MAP.get(fa, en) if fa in BADGE_MAP else en

    def clean_badge_secondary_en(self):
        fa = self.cleaned_data.get('badge_secondary') or ''
        en = (self.cleaned_data.get('badge_secondary_en') or '').strip()
        return BADGE_MAP.get(fa, en) if fa in BADGE_MAP else en

    def clean_price_label_en(self):
        fa = self.cleaned_data.get('price_label') or ''
        en = (self.cleaned_data.get('price_label_en') or '').strip()
        return PRICE_LABEL_MAP.get(fa, en) if fa in PRICE_LABEL_MAP else en


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'image_url', 'caption', 'caption_en', 'sort_order']
        widgets = {
            'image_url': forms.URLInput(attrs={
                'class': CSS_INPUT,
                'placeholder': 'https://...',
            }),
            'caption': forms.TextInput(attrs={'class': CSS_INPUT}),
            'caption_en': forms.TextInput(attrs={'class': CSS_INPUT}),
            'sort_order': forms.NumberInput(attrs={
                'class': 'w-20 border border-[#c1c8c4] rounded-lg px-2 py-1.5 text-sm',
                'min': 0,
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
