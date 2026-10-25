from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import get_language

from core.constants import Department


_FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def _persian_num(s):
    return str(s).translate(_FA_DIGITS)


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

    class PublishStatus(models.TextChoices):
        PENDING = 'pending', 'در انتظار تأیید مدیر'
        APPROVED = 'approved', 'تأیید و منتشر'
        REJECTED = 'rejected', 'رد شده'

    code = models.CharField('کد ملک', max_length=32, unique=True)
    title = models.CharField('عنوان (فارسی)', max_length=200)
    title_en = models.CharField('عنوان (انگلیسی)', max_length=200, blank=True)
    slug = models.SlugField('اسلاگ', max_length=220, unique=True, blank=True)

    department = models.CharField(
        'بخش',
        max_length=20,
        choices=Department.CHOICES,
        default=Department.SALE,
        db_index=True,
    )

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
    floor_en = models.CharField('طبقه (انگلیسی)', max_length=40, blank=True)
    year_built = models.CharField('سال ساخت', max_length=40, blank=True)
    year_built_en = models.CharField('سال ساخت (انگلیسی)', max_length=40, blank=True)

    price = models.BigIntegerField('قیمت (تومان)', default=0, help_text='عدد خام به تومان')
    price_label = models.CharField(
        'برچسب قیمت (فارسی)',
        max_length=80,
        blank=True,
        help_text='مثلاً توافقی — در صورت پر بودن به‌جای عدد',
    )
    price_label_en = models.CharField(
        'برچسب قیمت (انگلیسی)',
        max_length=80,
        blank=True,
        help_text='e.g. Negotiable',
    )

    agency_name = models.CharField('نام دفتر املاک', max_length=120, blank=True)
    agency_name_en = models.CharField('نام دفتر (انگلیسی)', max_length=120, blank=True)
    consultant_name = models.CharField('نام مشاور', max_length=120, blank=True)
    consultant_name_en = models.CharField('نام مشاور (انگلیسی)', max_length=120, blank=True)
    consultant_phone = models.CharField('تلفن مشاور', max_length=40, blank=True)

    badge_primary = models.CharField('نشان اصلی', max_length=60, blank=True)
    badge_primary_en = models.CharField('نشان اصلی (انگلیسی)', max_length=60, blank=True)
    badge_secondary = models.CharField('نشان فرعی', max_length=60, blank=True)
    badge_secondary_en = models.CharField('نشان فرعی (انگلیسی)', max_length=60, blank=True)

    cover_image = models.ImageField('تصویر اصلی', upload_to='properties/%Y/%m/', blank=True, null=True)
    cover_image_url = models.URLField('لینک تصویر جایگزین', blank=True)
    image_count = models.PositiveSmallIntegerField('تعداد تصاویر (دستی)', default=0)

    has_deed = models.BooleanField('سند تک‌برگ', default=True)
    is_complex_office = models.BooleanField('مستقر در مجموعه امتیاز', default=True)
    has_pool_or_roof = models.BooleanField('استخر / روف‌گاردن', default=False)
    is_brand_builder = models.BooleanField('سازنده برند', default=False)

    is_active = models.BooleanField('فعال / نمایش عمومی', default=False, db_index=True)
    is_featured = models.BooleanField('ویژه', default=False)
    is_exclusive = models.BooleanField('انحصاری مجموعه', default=False)

    publish_status = models.CharField(
        'وضعیت انتشار',
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.PENDING,
        db_index=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties_created',
        verbose_name='ثبت‌کننده',
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties_reviewed',
        verbose_name='تأییدکننده',
    )
    reviewed_at = models.DateTimeField('زمان بررسی', null=True, blank=True)
    review_note = models.CharField('یادداشت بررسی', max_length=255, blank=True)

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
        # فقط املاک تأییدشده می‌توانند فعال/عمومی باشند
        if self.publish_status != self.PublishStatus.APPROVED:
            self.is_active = False
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('real_estate:detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        return self.publish_status == self.PublishStatus.APPROVED and self.is_active

    def approve_publish(self, by_user, note=''):
        from django.utils import timezone
        self.publish_status = self.PublishStatus.APPROVED
        self.is_active = True
        self.reviewed_by = by_user
        self.reviewed_at = timezone.now()
        self.review_note = note or ''
        self.save(update_fields=[
            'publish_status', 'is_active', 'reviewed_by', 'reviewed_at',
            'review_note', 'updated_at',
        ])

    def reject_publish(self, by_user, note=''):
        from django.utils import timezone
        self.publish_status = self.PublishStatus.REJECTED
        self.is_active = False
        self.reviewed_by = by_user
        self.reviewed_at = timezone.now()
        self.review_note = note or ''
        self.save(update_fields=[
            'publish_status', 'is_active', 'reviewed_by', 'reviewed_at',
            'review_note', 'updated_at',
        ])

    @property
    def display_image(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        first = self.images.first()
        if first:
            return first.url
        return ''

    def gallery_urls(self):
        urls = []
        if self.cover_image:
            urls.append(self.cover_image.url)
        elif self.cover_image_url:
            urls.append(self.cover_image_url)
        for img in self.images.all():
            u = img.url
            if u and u not in urls:
                urls.append(u)
        return urls

    def gallery_count(self):
        n = len(self.gallery_urls())
        return max(n, self.image_count or 0)

    def formatted_price(self, lang=None):
        if lang is None:
            lang = (get_language() or 'fa')[:2]
        if lang == 'en' and self.price_label_en:
            return self.price_label_en
        if self.price_label and lang != 'en':
            return self.price_label
        if lang == 'en' and self.price_label and not self.price_label_en:
            return self.price_label
        if not self.price:
            return '—'
        formatted = f'{self.price:,}'
        if lang != 'en':
            return _persian_num(formatted)
        return formatted

    @property
    def formatted_price_en(self):
        return self.formatted_price(lang='en')

    def transaction_label_en(self):
        mapping = {
            'sale': 'For sale',
            'rent': 'For rent',
            'presale': 'Pre-sale',
            'partnership': 'Partnership',
        }
        return mapping.get(self.transaction_type, self.get_transaction_type_display())

    def property_type_label_en(self):
        mapping = {
            'penthouse': 'Penthouse / Super-luxury',
            'apartment': 'Residential apartment',
            'villa': 'Villa / Mansion',
            'office': 'Office',
            'commercial': 'Commercial',
        }
        return mapping.get(self.property_type, self.get_property_type_display())


class PropertyImage(models.Model):
    listing = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='ملک',
    )
    image = models.ImageField('فایل تصویر', upload_to='properties/gallery/%Y/%m/', blank=True, null=True)
    image_url = models.URLField('لینک تصویر', blank=True, help_text='اگر فایل آپلود نشد')
    caption = models.CharField('عنوان (فارسی)', max_length=120, blank=True)
    caption_en = models.CharField('عنوان (انگلیسی)', max_length=120, blank=True)
    sort_order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        verbose_name = 'تصویر ملک'
        verbose_name_plural = 'تصاویر ملک'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.listing.code} — image {self.pk}'

    @property
    def url(self):
        if self.image:
            return self.image.url
        return self.image_url or ''
