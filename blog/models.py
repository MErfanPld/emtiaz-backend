from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import get_language

from ckeditor.fields import RichTextField


def _is_en(lang=None):
    return ((lang or get_language() or 'fa')[:2] == 'en')


class Category(models.Model):
    name = models.CharField('نام دسته', max_length=80)
    name_en = models.CharField('نام انگلیسی', max_length=80, blank=True)
    slug = models.SlugField('اسلاگ', max_length=100, unique=True, blank=True, allow_unicode=True)
    sort_order = models.PositiveIntegerField('ترتیب', default=0)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'دسته‌بندی مقاله'
        verbose_name_plural = 'دسته‌بندی مقالات'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name, allow_unicode=True)[:100] or f'cat-{self.pk or "new"}'
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        if _is_en() and self.name_en:
            return self.name_en
        return self.name


class Tag(models.Model):
    name = models.CharField('نام برچسب', max_length=60)
    name_en = models.CharField('نام انگلیسی', max_length=60, blank=True)
    slug = models.SlugField('اسلاگ', max_length=80, unique=True, blank=True, allow_unicode=True)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name, allow_unicode=True)[:80] or f'tag-{self.pk or "new"}'
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        if _is_en() and self.name_en:
            return self.name_en
        return self.name


class Post(models.Model):
    title = models.CharField('عنوان', max_length=220)
    title_en = models.CharField('عنوان انگلیسی', max_length=220, blank=True)
    slug = models.SlugField('اسلاگ', max_length=240, unique=True, blank=True, allow_unicode=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='دسته‌بندی',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='برچسب‌ها')
    excerpt = models.TextField('خلاصه', blank=True)
    excerpt_en = models.TextField('خلاصه انگلیسی', blank=True)
    body = RichTextField('متن کامل', config_name='default')
    body_en = RichTextField('متن انگلیسی', config_name='body_en', blank=True)
    cover_image = models.ImageField('تصویر کاور', upload_to='blog/%Y/%m/', blank=True, null=True)
    cover_image_url = models.URLField('لینک تصویر جایگزین', blank=True)
    author_name = models.CharField('نویسنده', max_length=120, default='تیم تحریریه املاک امتیاز')
    author_name_en = models.CharField('نویسنده انگلیسی', max_length=120, blank=True, default='Emtiaz Editorial Team')
    reading_minutes = models.PositiveSmallIntegerField('زمان مطالعه (دقیقه)', default=5)
    is_published = models.BooleanField('منتشر شده', default=False, db_index=True)
    is_featured = models.BooleanField('ویژه', default=False)
    published_at = models.DateTimeField('تاریخ انتشار', null=True, blank=True)
    views_count = models.PositiveIntegerField('بازدید', default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts',
        verbose_name='ایجادکننده',
    )
    created_at = models.DateTimeField('ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('به‌روزرسانی', auto_now=True)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_en or self.title, allow_unicode=True) or 'post'
            self.slug = base[:230]
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    @property
    def display_image(self):
        if self.cover_image:
            return self.cover_image.url
        return self.cover_image_url or ''

    @property
    def display_title(self):
        if _is_en() and self.title_en:
            return self.title_en
        return self.title

    @property
    def display_excerpt(self):
        if _is_en() and self.excerpt_en:
            return self.excerpt_en
        return self.excerpt

    @property
    def display_body(self):
        if _is_en() and self.body_en:
            return self.body_en
        return self.body

    @property
    def display_author(self):
        if _is_en() and self.author_name_en:
            return self.author_name_en
        return self.author_name
