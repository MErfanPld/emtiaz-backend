import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='نام دسته')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=100, unique=True, verbose_name='اسلاگ')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='ترتیب')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={
                'verbose_name': 'دسته‌بندی مقاله',
                'verbose_name_plural': 'دسته‌بندی مقالات',
                'ordering': ['sort_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=240, unique=True, verbose_name='اسلاگ')),
                ('excerpt', models.TextField(blank=True, verbose_name='خلاصه')),
                ('body', models.TextField(help_text='می‌توانید از HTML ساده استفاده کنید.', verbose_name='متن کامل')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m/', verbose_name='تصویر کاور')),
                ('cover_image_url', models.URLField(blank=True, verbose_name='لینک تصویر جایگزین')),
                ('author_name', models.CharField(default='تیم تحریریه املاک امتیاز', max_length=120, verbose_name='نویسنده')),
                ('reading_minutes', models.PositiveSmallIntegerField(default=5, verbose_name='زمان مطالعه (دقیقه)')),
                ('tags', models.CharField(blank=True, help_text='با ویرگول جدا کنید', max_length=255, verbose_name='برچسب‌ها')),
                ('is_published', models.BooleanField(db_index=True, default=False, verbose_name='منتشر شده')),
                ('is_featured', models.BooleanField(default=False, verbose_name='ویژه')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انتشار')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='بازدید')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='به‌روزرسانی')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.category', verbose_name='دسته‌بندی')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_posts', to=settings.AUTH_USER_MODEL, verbose_name='ایجادکننده')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
                'ordering': ['-published_at', '-created_at'],
            },
        ),
    ]
