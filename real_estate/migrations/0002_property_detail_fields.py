from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='year_built',
            field=models.CharField(blank=True, max_length=40, verbose_name='سال ساخت'),
        ),
        migrations.AddField(
            model_name='property',
            name='consultant_name',
            field=models.CharField(blank=True, max_length=120, verbose_name='نام مشاور'),
        ),
        migrations.AddField(
            model_name='property',
            name='consultant_phone',
            field=models.CharField(blank=True, max_length=40, verbose_name='تلفن مشاور'),
        ),
    ]
