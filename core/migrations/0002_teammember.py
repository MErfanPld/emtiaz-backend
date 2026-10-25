from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_consultation'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('co_director', 'مدیر مجموعه'), ('dept_manager', 'مدیر بخش')], db_index=True, default='dept_manager', max_length=20, verbose_name='نقش')),
                ('department', models.CharField(blank=True, choices=[('rent', 'رهن و اجاره'), ('sale', 'خرید و فروش'), ('kolangi', 'کلنگی'), ('partnership', 'مشارکت در ساخت'), ('mostaghelat', 'مستقلات')], default='', help_text='فقط برای مدیر بخش', max_length=20, verbose_name='بخش')),
                ('name', models.CharField(max_length=120, verbose_name='نام (فارسی)')),
                ('name_en', models.CharField(blank=True, max_length=120, verbose_name='نام (انگلیسی)')),
                ('title', models.CharField(blank=True, max_length=160, verbose_name='سمت (فارسی)')),
                ('title_en', models.CharField(blank=True, max_length=160, verbose_name='سمت (انگلیسی)')),
                ('bio', models.TextField(blank=True, verbose_name='توضیح کوتاه (فارسی)')),
                ('bio_en', models.TextField(blank=True, verbose_name='توضیح کوتاه (انگلیسی)')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='team/%Y/%m/', verbose_name='تصویر')),
                ('photo_url', models.URLField(blank=True, verbose_name='لینک تصویر جایگزین')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='ترتیب')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'عضو تیم مدیریت',
                'verbose_name_plural': 'تیم مدیریت',
                'ordering': ['role', 'sort_order', 'id'],
            },
        ),
    ]
