from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, unique=True, verbose_name='کد ملک')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان (فارسی)')),
                ('title_en', models.CharField(blank=True, max_length=200, verbose_name='عنوان (انگلیسی)')),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True, verbose_name='اسلاگ')),
                ('transaction_type', models.CharField(choices=[('sale', 'خرید و فروش'), ('rent', 'رهن و اجاره'), ('presale', 'پیش‌فروش'), ('partnership', 'مشارکت در ساخت')], db_index=True, default='sale', max_length=20, verbose_name='نوع معامله')),
                ('property_type', models.CharField(choices=[('penthouse', 'پنت‌هاوس و سوپرلوکس'), ('apartment', 'آپارتمان مسکونی'), ('villa', 'ویلا / عمارت'), ('office', 'اداری'), ('commercial', 'تجاری')], db_index=True, default='apartment', max_length=20, verbose_name='نوع کاربری')),
                ('area_name', models.CharField(max_length=120, verbose_name='محدوده / محله')),
                ('area_name_en', models.CharField(blank=True, max_length=120, verbose_name='محدوده (انگلیسی)')),
                ('address_line', models.CharField(blank=True, max_length=255, verbose_name='آدرس کوتاه')),
                ('address_line_en', models.CharField(blank=True, max_length=255, verbose_name='آدرس کوتاه (انگلیسی)')),
                ('area_sqm', models.PositiveIntegerField(default=0, verbose_name='متراژ (متر مربع)')),
                ('bedrooms', models.PositiveSmallIntegerField(default=0, verbose_name='تعداد خواب')),
                ('parking', models.PositiveSmallIntegerField(default=0, verbose_name='پارکینگ')),
                ('floor', models.CharField(blank=True, max_length=40, verbose_name='طبقه')),
                ('price', models.BigIntegerField(default=0, help_text='عدد خام به تومان', verbose_name='قیمت (تومان)')),
                ('price_label', models.CharField(blank=True, help_text='در صورت پر بودن به‌جای عدد نمایش داده می‌شود', max_length=80, verbose_name='برچسب قیمت سفارشی')),
                ('agency_name', models.CharField(blank=True, max_length=120, verbose_name='نام دفتر املاک')),
                ('agency_name_en', models.CharField(blank=True, max_length=120, verbose_name='نام دفتر (انگلیسی)')),
                ('badge_primary', models.CharField(blank=True, help_text='مثلاً فروش انحصاری', max_length=60, verbose_name='نشان اصلی')),
                ('badge_secondary', models.CharField(blank=True, max_length=60, verbose_name='نشان فرعی')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='properties/%Y/%m/', verbose_name='تصویر اصلی')),
                ('cover_image_url', models.URLField(blank=True, help_text='اگر فایل آپلود نشد', verbose_name='لینک تصویر جایگزین')),
                ('image_count', models.PositiveSmallIntegerField(default=1, verbose_name='تعداد تصاویر')),
                ('has_deed', models.BooleanField(default=True, verbose_name='سند تک‌برگ')),
                ('is_complex_office', models.BooleanField(default=True, verbose_name='مستقر در مجتمع امتیاز')),
                ('has_pool_or_roof', models.BooleanField(default=False, verbose_name='استخر / روف‌گاردن')),
                ('is_brand_builder', models.BooleanField(default=False, verbose_name='سازنده برند')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='فعال / نمایش عمومی')),
                ('is_featured', models.BooleanField(default=False, verbose_name='ویژه')),
                ('is_exclusive', models.BooleanField(default=False, verbose_name='انحصاری مجتمع')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات (فارسی)')),
                ('description_en', models.TextField(blank=True, verbose_name='توضیحات (انگلیسی)')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='به‌روزرسانی')),
            ],
            options={
                'verbose_name': 'ملک',
                'verbose_name_plural': 'املاک',
                'ordering': ['-is_featured', 'sort_order', '-created_at'],
            },
        ),
    ]
