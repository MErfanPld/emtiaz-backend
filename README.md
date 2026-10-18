# Emtiaz Backend

Backend و سایت املاک امتیاز — Django Templates + Session Authentication

## راه‌اندازی

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # با ایمیل
python manage.py runserver
```

## احراز هویت (کلاسیک / Session)

| مسیر | توضیح |
|------|--------|
| `/accounts/login/` | ورود (فقط حساب تأییدشده و فعال) |
| `/accounts/logout/` | خروج امن (فقط POST + CSRF) |
| `/accounts/register/` | ثبت‌نام (حساب همیشه pending) |
| `/accounts/register/done/` | پیام موفقیت ثبت‌نام |
| `/accounts/pending/` | صفحه انتظار تأیید / رد |
| `/accounts/profile/` | مشاهده و ویرایش پروفایل |
| `/accounts/password/change/` | تغییر رمز عبور |
| `/dashboard/` | داشبورد (نیاز به ورود + تأیید) |
| `/admin/` | پنل ادمین Django |

## قوانین امنیتی

- ثبت‌نام هرگز حساب را خودکار تأیید نمی‌کند.
- `approval_status` از `is_active` جدا است.
- کاربر pending / rejected / inactive وارد صفحات محافظت‌شده نمی‌شود.
- خروج فقط با POST و CSRF.
- کاربر نمی‌تواند نقش یا وضعیت تأیید خود را تغییر دهد.
- تأیید/رد حساب فقط از طریق Django Admin.
