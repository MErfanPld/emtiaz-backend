# مجموعه املاک امتیاز (Emtiaz)

سایت و پنل مدیریت املاک امتیاز — **Django Templates** + **Session Authentication**

## پیش‌نیاز

- Python 3.12+
- pip / venv

## راه‌اندازی

```bash
git pull origin master
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # در صورت نیاز
python manage.py migrate
python manage.py createsuperuser   # ورود با شماره موبایل
python manage.py runserver
```

- سایت: http://127.0.0.1:8000/
- داشبورد: http://127.0.0.1:8000/dashboard/
- ادمین: http://127.0.0.1:8000/admin/

### (اختیاری) جمع‌آوری استاتیک برای production

```bash
python manage.py collectstatic --noinput
# خروجی در static_cdn/ قرار می‌گیرد و در git نادیده گرفته می‌شود
```

## ساختار اصلی

| مسیر | توضیح |
|------|--------|
| `accounts/` | کاربر سفارشی (موبایل)، ورود/ثبت‌نام، تأیید حساب |
| `core/` | صفحه اصلی، درباره، درخواست مشاوره |
| `real_estate/` | لیست و جزئیات املاک + گالری |
| `blog/` | مقالات (CKEditor، دسته، برچسب) |
| `dashboard/` | پنل مدیریت (املاک، وبلاگ، کاربران، مشاوره) |
| `assets/` | استاتیک منبع (CSS / JS / تصاویر) |
| `templates/` | قالب‌های مشترک، حساب کاربری و داشبورد |

## وابستگی‌ها

- Django 6.x
- Pillow
- django-ckeditor
- jdatetime

## نکات

- احراز هویت: Session (بدون REST/JWT)
- ثبت‌نام → وضعیت `pending` تا تأیید مدیر
- زبان: فارسی پیش‌فرض + انگلیسی (`/en/`)
- اعداد و تاریخ‌ها فارسی (فیلتر + JS)
- پیامک مشاوره فعلاً تستی در کنسول چاپ می‌شود
- `static_cdn/` در `.gitignore` است (خروجی collectstatic و media)
