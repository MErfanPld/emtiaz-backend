import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('real_estate', '0005_alter_property_is_complex_office_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='department',
            field=models.CharField(
                choices=[
                    ('rent', 'رهن و اجاره'),
                    ('sale', 'خرید و فروش'),
                    ('kolangi', 'کلنگی'),
                    ('partnership', 'مشارکت در ساخت'),
                    ('mostaghelat', 'مستقلات'),
                ],
                db_index=True,
                default='sale',
                max_length=20,
                verbose_name='بخش',
            ),
        ),
        migrations.AddField(
            model_name='property',
            name='publish_status',
            field=models.CharField(
                choices=[
                    ('pending', 'در انتظار تأیید مدیر'),
                    ('approved', 'تأیید و منتشر'),
                    ('rejected', 'رد شده'),
                ],
                db_index=True,
                default='pending',
                max_length=20,
                verbose_name='وضعیت انتشار',
            ),
        ),
        migrations.AddField(
            model_name='property',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='properties_created',
                to=settings.AUTH_USER_MODEL,
                verbose_name='ثبت‌کننده',
            ),
        ),
        migrations.AddField(
            model_name='property',
            name='reviewed_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='properties_reviewed',
                to=settings.AUTH_USER_MODEL,
                verbose_name='تأییدکننده',
            ),
        ),
        migrations.AddField(
            model_name='property',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='زمان بررسی'),
        ),
        migrations.AddField(
            model_name='property',
            name='review_note',
            field=models.CharField(blank=True, max_length=255, verbose_name='یادداشت بررسی'),
        ),
        # املاک قبلی را تأییدشده در نظر بگیر
        migrations.RunPython(
            code=lambda apps, schema_editor: apps.get_model('real_estate', 'Property').objects.update(
                publish_status='approved'
            ),
            reverse_code=migrations.RunPython.noop,
        ),
    ]
