from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ConsultationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=120, verbose_name='نام و نام خانوادگی')),
                ('phone', models.CharField(max_length=20, verbose_name='شماره تماس')),
                ('request_type', models.CharField(choices=[('buy', 'خرید آپارتمان / پنت‌هاوس'), ('sell', 'فروش یا تهاتر ملک شخصی'), ('rent', 'استیجار واحد اداری یا تجاری'), ('invest', 'مشاوره سرمایه‌گذاری و مشارکت در ساخت'), ('other', 'سایر')], default='buy', max_length=20, verbose_name='نوع درخواست')),
                ('message', models.TextField(blank=True, verbose_name='توضیح اختیاری')),
                ('status', models.CharField(choices=[('new', 'جدید'), ('contacted', 'تماس گرفته شد'), ('done', 'انجام شد'), ('archived', 'بایگانی')], db_index=True, default='new', max_length=20, verbose_name='وضعیت')),
                ('admin_note', models.TextField(blank=True, verbose_name='یادداشت مدیر')),
                ('sms_sent', models.BooleanField(default=False, verbose_name='پیامک به مدیر ارسال شد')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='به‌روزرسانی')),
            ],
            options={
                'verbose_name': 'درخواست مشاوره',
                'verbose_name_plural': 'درخواست‌های مشاوره',
                'ordering': ['-created_at'],
            },
        ),
    ]
