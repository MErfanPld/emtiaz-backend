from django.db import models

from core.constants import Department


class ConsultationRequest(models.Model):
    """درخواست مشاوره از صفحه اصلی."""

    class RequestType(models.TextChoices):
        BUY = 'buy', 'خرید آپارتمان / پنت‌هاوس'
        SELL = 'sell', 'فروش یا تهاتر ملک شخصی'
        RENT = 'rent', 'استیجار واحد اداری یا تجاری'
        INVEST = 'invest', 'مشاوره سرمایه‌گذاری و مشارکت در ساخت'
        OTHER = 'other', 'سایر'

    class Status(models.TextChoices):
        NEW = 'new', 'جدید'
        CONTACTED = 'contacted', 'تماس گرفته شد'
        DONE = 'done', 'انجام شد'
        ARCHIVED = 'archived', 'بایگانی'

    full_name = models.CharField('نام و نام خانوادگی', max_length=120)
    phone = models.CharField('شماره تماس', max_length=20)
    request_type = models.CharField(
        'نوع درخواست',
        max_length=20,
        choices=RequestType.choices,
        default=RequestType.BUY,
    )
    message = models.TextField('توضیح اختیاری', blank=True)
    status = models.CharField(
        'وضعیت',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    admin_note = models.TextField('یادداشت مدیر', blank=True)
    sms_sent = models.BooleanField('پیامک به مدیر ارسال شد', default=False)
    created_at = models.DateTimeField('زمان ثبت', auto_now_add=True)
    updated_at = models.DateTimeField('به‌روزرسانی', auto_now=True)

    class Meta:
        verbose_name = 'درخواست مشاوره'
        verbose_name_plural = 'درخواست‌های مشاوره'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} — {self.phone}'


class TeamMember(models.Model):
    """مدیران مجموعه و مدیران بخش‌ها (صفحه اصلی / معرفی)."""

    class Role(models.TextChoices):
        CO_DIRECTOR = 'co_director', 'مدیر مجموعه'
        DEPT_MANAGER = 'dept_manager', 'مدیر بخش'

    role = models.CharField(
        'نقش',
        max_length=20,
        choices=Role.choices,
        default=Role.DEPT_MANAGER,
        db_index=True,
    )
    department = models.CharField(
        'بخش',
        max_length=20,
        choices=Department.CHOICES,
        blank=True,
        default='',
        help_text='فقط برای مدیر بخش',
    )
    name = models.CharField('نام (فارسی)', max_length=120)
    name_en = models.CharField('نام (انگلیسی)', max_length=120, blank=True)
    title = models.CharField('سمت (فارسی)', max_length=160, blank=True)
    title_en = models.CharField('سمت (انگلیسی)', max_length=160, blank=True)
    bio = models.TextField('توضیح کوتاه (فارسی)', blank=True)
    bio_en = models.TextField('توضیح کوتاه (انگلیسی)', blank=True)
    photo = models.ImageField('تصویر', upload_to='team/%Y/%m/', blank=True, null=True)
    photo_url = models.URLField('لینک تصویر جایگزین', blank=True)
    is_active = models.BooleanField('فعال', default=True)
    sort_order = models.PositiveIntegerField('ترتیب', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'عضو تیم مدیریت'
        verbose_name_plural = 'تیم مدیریت'
        ordering = ['role', 'sort_order', 'id']

    def __str__(self):
        return f'{self.name} ({self.get_role_display()})'

    @property
    def display_photo(self):
        if self.photo:
            return self.photo.url
        return self.photo_url or ''

    def department_label(self, lang='fa'):
        if not self.department:
            return ''
        if lang == 'en':
            return Department.CHOICES_EN.get(self.department, self.department)
        return dict(Department.CHOICES).get(self.department, self.department)

    @property
    def department_label_en(self):
        return self.department_label(lang='en')
