from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Property(models.Model):
    """ملک قابل نمایش در لیست عمومی و مدیریت از پنل ادمین."""

    class TransactionType(models.TextChoices):
        SALE = 'sale', 'خرید و فروش'
        RENT = 'rent', 'رهن و اجاره'
        PRESALE = 'presale', 'پیش‌فروش'
        PARTNERSHIP = 'partnership', 'مشارکت در ساخت'

    class PropertyType(models.TextChoices):
        PENTHOUSE = 'penthouse', 'پنت‌هاوس و سوپرلوکس'
        APARTMENT = 'apartment', 'آپارتمان مسکونی'
        VILLA = 'villa', 'ویلا / عمارت'
        OFFICE = 'office', 'اداری'
        COMMERCIAL = 'commercial', 'تجاری'

    code = models.CharField('کد ملک', max_length=32, unique=True)
    title = models.CharField('عنوان (فارسی)', max_length=200)
    title_en = models.CharField('عنوان (انگلیسی)', max_length=200, blank=True)
    slug = models.SlugField('اسلاگ', max_length=220, unique=True, blank=True)

    transaction_type = models.CharField(
        'نوع معامله',
        max_length=20,
        choices=TransactionType.choices,
        default=TransactionType.SALE,
        db_index=True,
    )
    property_type = models.CharField(
        'نوع کاربری',
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
        db_index=True,
    )

    area_name = models.CharField('محدوده / محله', max_length=120)
    area_name_en = models.CharField('محدوده (انگلیسی)', max_length=120, blank=True)
    address_line = models.CharField('آدرس کوتاه', max_length=255, blank=True)
    address_line_en = models.CharField('آدرس کوتاه (انگلیسی)', max_length=255, blank=True)

    area_sqm = models.PositiveIntegerField('متراژ (متر مربع)', default=0)
    bedrooms = models.PositiveSmallIntegerField('تعداد خواب', default=0)
    parking = models.PositiveSmallIntegerField('پارکینگ', default=0)
    floor = models.CharField('طبقه', max_length=40, blank=True)
    year_built = models.CharField('سال ساخت', max_length=40, blank=True)

    price = models.BigIntegerField('قیمت (تومان)', default=0, help_text='عدد خام به تومان')
    price_label = models.CharField(
        'برچسب قیمت سفارشی',
        max_length=80,
        blank=True,
        help_text='در صورت پر بودن به‌جای عدد نمایش داده می‌شود',
    )

    agency_name = models.CharField('نام دفتر املاک', max_length=120, blank=True)
    agency_name_en = models.CharField('نام دفتر (انگلیسی)', max_length=120, blank=True)
    consultant_name = models.CharField('نام مشاور', max_length=120, blank=True)
    consultant_phone = models.CharField('تلفن مشاور', max_length=40, blank=True)

    badge_primary = models.CharField('نشان اصلی', max_length=60, blank=True, help_text='مثلاً فروش انحصاری')
    badge_secondary = models.CharField('نشان فرعی', max_length=60, blank=True)

    cover_image = models.ImageField('تصویر اصلی', upload_to='properties/%Y/%m/', blank=True, null=True)
    cover_image_url = models.URLField('لینک تصویر جایگزین', blank=True, help_text='اگر فایل آپلود نشد')
    image_count = models.PositiveSmallIntegerField('تعداد تصاویر', default=1)

    has_deed = models.BooleanField('سند تک‌برگ', default=True)
    is_complex_office = models.BooleanField('مستقر در مجتمع امتیاز', default=True)
    has_pool_or_roof = models.BooleanField('استخر / روف‌گاردن', default=False)
    is_brand_builder = models.BooleanField('سازنده برند', default=False)

    is_active = models.BooleanField('فعال / نمایش عمومی', default=True, db_index=True)
    is_featured = models.BooleanField('ویژه', default=False)
    is_exclusive = models.BooleanField('انحصاری مجتمع', default=False)

    description = models.TextField('توضیحات (فارسی)', blank=True)
    description_en = models.TextField('توضیحات (انگلیسی)', blank=True)

    sort_order = models.PositiveIntegerField('ترتیب نمایش', default=0)
    created_at = models.DateTimeField('ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('به‌روزرسانی', auto_now=True)

    class Meta:
        verbose_name = 'ملک'
        verbose_name_plural = 'املاک'
        ordering = ['-is_featured', 'sort_order', '-created_at']

    def __str__(self):
        return f'{self.code} — {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_en or self.title, allow_unicode=True) or self.code
            self.slug = f'{base}-{self.code}'.lower()[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('real_estate:detail', kwargs={'slug': self.slug})

    @property
    def display_image(self):
        if self.cover_image:
            return self.cover_image.url
        return self.cover_image_url or ''

    def formatted_price(self):
        if self.price_label:
            return self.price_label
        if not self.price:
            return '—'
        return f'{self.price:,}'

    def transaction_label_en(self):
        mapping = {
            'sale': 'For sale',
            'rent': 'For rent',
            'presale': 'Pre-sale',
            'partnership': 'Partnership',
        }
        return mapping.get(self.transaction_type, self.get_transaction_type_display())
