from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('نام دسته', max_length=80)
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
            self.slug = slugify(self.name, allow_unicode=True)[:100] or f'cat-{self.pk or "new"}'
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField('عنوان', max_length=220)
    slug = models.SlugField('اسلاگ', max_length=240, unique=True, blank=True, allow_unicode=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='دسته‌بندی',
    )
    excerpt = models.TextField('خلاصه', blank=True)
    body = models.TextField('متن کامل', help_text='می‌توانید از HTML ساده استفاده کنید.')
    cover_image = models.ImageField('تصویر کاور', upload_to='blog/%Y/%m/', blank=True, null=True)
    cover_image_url = models.URLField('لینک تصویر جایگزین', blank=True)
    author_name = models.CharField('نویسنده', max_length=120, default='تیم تحریریه املاک امتیاز')
    reading_minutes = models.PositiveSmallIntegerField('زمان مطالعه (دقیقه)', default=5)
    tags = models.CharField('برچسب‌ها', max_length=255, blank=True, help_text='با ویرگول جدا کنید')
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
            base = slugify(self.title, allow_unicode=True) or 'post'
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

    def tag_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]
