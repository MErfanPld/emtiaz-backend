import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='نام برچسب')),
                ('name_en', models.CharField(blank=True, max_length=60, verbose_name='نام انگلیسی')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=80, unique=True, verbose_name='اسلاگ')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب‌ها',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, max_length=80, verbose_name='نام انگلیسی'),
        ),
        migrations.AddField(
            model_name='post',
            name='author_name_en',
            field=models.CharField(blank=True, default='Emtiaz Editorial Team', max_length=120, verbose_name='نویسنده انگلیسی'),
        ),
        migrations.AddField(
            model_name='post',
            name='body_en',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='متن انگلیسی'),
        ),
        migrations.AddField(
            model_name='post',
            name='excerpt_en',
            field=models.TextField(blank=True, verbose_name='خلاصه انگلیسی'),
        ),
        migrations.AddField(
            model_name='post',
            name='title_en',
            field=models.CharField(blank=True, max_length=220, verbose_name='عنوان انگلیسی'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name='متن کامل'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='blog.tag', verbose_name='برچسب‌ها'),
        ),
    ]
