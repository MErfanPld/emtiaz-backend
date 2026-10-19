from django.db import models


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
