# Emtiaz Backend

Backend سیستم املاک امتیاز — Django + DRF + SimpleJWT

## راه‌اندازی سریع

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# ویرایش .env در صورت نیاز
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Accounts (نسخه v1)

Base: `/api/v1/accounts/`

| Method | Endpoint | دسترسی | توضیح |
|--------|----------|--------|-------|
| POST | `/register/` | Public | ثبت‌نام (حساب pending) |
| POST | `/login/` | Public | ورود (فقط approved + active) |
| POST | `/logout/` | Auth | ابطال refresh token |
| POST | `/token/refresh/` | Public | تمدید access token |
| GET/PATCH | `/me/` | Approved | پروفایل کاربر جاری |
| POST | `/change-password/` | Approved | تغییر رمز |
| GET | `/users/` | Admin/Manager | فهرست کاربران |
| GET | `/users/pending/` | Admin/Manager | حساب‌های در انتظار تأیید |
| POST | `/users/{id}/approve/` | Admin | تأیید حساب |
| POST | `/users/{id}/reject/` | Admin | رد حساب (با reason) |
| POST | `/users/{id}/activate/` | Admin | فعال‌سازی |
| POST | `/users/{id}/deactivate/` | Admin | غیرفعال‌سازی |

## نکات امنیتی

- ثبت‌نام هرگز `is_staff` / `is_superuser` / `approval_status` را از ورودی قبول نمی‌کند.
- حساب pending یا inactive حتی با توکن معتبر به endpointهای محافظت‌شده دسترسی ندارد (`IsApproved`).
- تغییر وضعیت حساب (approve / deactivate) بلافاصله روی درخواست‌های بعدی اعمال می‌شود.
