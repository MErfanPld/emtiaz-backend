from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_teammember'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teammember',
            options={
                'ordering': ['sort_order', 'role', 'id'],
                'verbose_name': 'عضو تیم',
                'verbose_name_plural': 'تیم مجموعه',
            },
        ),
        migrations.AlterField(
            model_name='teammember',
            name='role',
            field=models.CharField(
                choices=[
                    ('co_director', 'مدیر مجموعه'),
                    ('dept_manager', 'مدیر بخش'),
                    ('member', 'عضو تیم'),
                ],
                db_index=True,
                default='member',
                max_length=20,
                verbose_name='دسته / نقش',
            ),
        ),
        migrations.AlterField(
            model_name='teammember',
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
                default='',
                help_text='اختیاری — مثلاً برای مدیر بخش یا مشاور همان بخش',
                max_length=20,
                verbose_name='بخش تخصصی',
            ),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال / نمایش در سایت'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش'),
        ),
    ]
