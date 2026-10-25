from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(
                blank=True,
                choices=[
                    ('rent', 'رهن و اجاره'),
                    ('sale', 'خرید و فروش'),
                    ('kolangi', 'کلنگی'),
                    ('partnership', 'مشارکت در ساخت'),
                    ('mostaghelat', 'مستقلات'),
                ],
                db_index=True,
                default='',
                help_text='کارمند فقط می‌تواند برای این بخش ملک ثبت کند.',
                max_length=20,
                verbose_name='بخش تخصصی',
            ),
        ),
    ]
