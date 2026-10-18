# Generated for phone-based custom User (USERNAME_FIELD=phone_number)

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='username')),
                ('phone_number', models.CharField(help_text='مثال: 09123456789', max_length=15, unique=True, verbose_name='شماره موبایل')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='ایمیل')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/%Y/%m/', verbose_name='تصویر پروفایل')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('personnel_code', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='کد پرسنلی')),
                ('job_title', models.CharField(blank=True, default='', max_length=100, verbose_name='عنوان شغلی')),
                ('branch', models.CharField(blank=True, default='', max_length=100, verbose_name='شعبه / واحد')),
                ('internal_notes', models.TextField(blank=True, default='', verbose_name='یادداشت داخلی')),
                ('approval_status', models.CharField(choices=[('pending', 'در انتظار تأیید'), ('approved', 'تأیید شده'), ('rejected', 'رد شده')], db_index=True, default='pending', max_length=20, verbose_name='وضعیت تأیید')),
                ('requested_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')),
                ('approved_at', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ تأیید / رد')),
                ('rejection_reason', models.TextField(blank=True, default='', verbose_name='دلیل رد')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_users', to=settings.AUTH_USER_MODEL, verbose_name='تأییدکننده')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to=settings.AUTH_USER_MODEL, verbose_name='مدیر مستقیم')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['approval_status', 'is_active'], name='accounts_us_approva_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['phone_number'], name='accounts_us_phone_idx'),
        ),
    ]
