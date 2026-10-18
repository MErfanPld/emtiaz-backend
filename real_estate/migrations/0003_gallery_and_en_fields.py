from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0002_property_detail_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='badge_primary_en',
            field=models.CharField(blank=True, max_length=60, verbose_name='نشان اصلی (انگلیسی)'),
        ),
        migrations.AddField(
            model_name='property',
            name='badge_secondary_en',
            field=models.CharField(blank=True, max_length=60, verbose_name='نشان فرعی (انگلیسی)'),
        ),
        migrations.AddField(
            model_name='property',
            name='consultant_name_en',
            field=models.CharField(blank=True, max_length=120, verbose_name='نام مشاور (انگلیسی)'),
        ),
        migrations.AddField(
            model_name='property',
            name='floor_en',
            field=models.CharField(blank=True, max_length=40, verbose_name='طبقه (انگلیسی)'),
        ),
        migrations.AddField(
            model_name='property',
            name='price_label_en',
            field=models.CharField(blank=True, help_text='e.g. Negotiable', max_length=80, verbose_name='برچسب قیمت (انگلیسی)'),
        ),
        migrations.AddField(
            model_name='property',
            name='year_built_en',
            field=models.CharField(blank=True, max_length=40, verbose_name='سال ساخت (انگلیسی)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_label',
            field=models.CharField(blank=True, help_text='مثلاً توافقی — در صورت پر بودن به‌جای عدد', max_length=80, verbose_name='برچسب قیمت (فارسی)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='image_count',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='تعداد تصاویر (دستی)'),
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='properties/gallery/%Y/%m/', verbose_name='فایل تصویر')),
                ('image_url', models.URLField(blank=True, help_text='اگر فایل آپلود نشد', verbose_name='لینک تصویر')),
                ('caption', models.CharField(blank=True, max_length=120, verbose_name='عنوان (فارسی)')),
                ('caption_en', models.CharField(blank=True, max_length=120, verbose_name='عنوان (انگلیسی)')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='ترتیب')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='real_estate.property', verbose_name='ملک')),
            ],
            options={
                'verbose_name': 'تصویر ملک',
                'verbose_name_plural': 'تصاویر ملک',
                'ordering': ['sort_order', 'id'],
            },
        ),
    ]
