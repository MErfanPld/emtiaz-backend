"""ارسال پیامک تستی — فعلاً فقط لاگ می‌شود."""
import logging

logger = logging.getLogger('core.sms')

# شماره مدیران برای اعلان (بعداً از تنظیمات بخوانید)
ADMIN_NOTIFY_PHONES = ['09120000000']


def send_sms(phone: str, message: str) -> bool:
    """شبیه‌سازی ارسال SMS — در لاگ و کنسول چاپ می‌شود."""
    text = f'[SMS-TEST] to={phone} | {message}'
    logger.info(text)
    print(text)
    return True


def notify_admins_new_consultation(req) -> bool:
    msg = (
        f'درخواست مشاوره جدید\n'
        f'نام: {req.full_name}\n'
        f'موبایل: {req.phone}\n'
        f'موضوع: {req.get_request_type_display()}'
    )
    ok = True
    for admin_phone in ADMIN_NOTIFY_PHONES:
        if not send_sms(admin_phone, msg):
            ok = False
    return ok
