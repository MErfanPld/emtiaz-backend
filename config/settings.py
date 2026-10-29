"""
Django settings for config project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "y65WcyGjNespblusMarvgTGPeBPT8GoV_35onZDymRjEITbZ4fbmc2_9UTpr37hqdBE"
DEBUG = os.environ.get("DEBUG", "False").lower() in (
    "1", "true", "yes", "on"
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "emtiazrealestate.com,www.emtiazrealestate.com"
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ckeditor',
    'ckeditor_uploader',

    'core',
    'blog',
    'accounts',
    'dashboard',
    'real_estate',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.dashboard_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fa'
LANGUAGES = [
    ('fa', 'فارسی'),
    ('en', 'English'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
USE_I18N = True
USE_TZ = True
TIME_ZONE = 'Asia/Tehran'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'assets']
STATIC_ROOT = BASE_DIR / 'static_cdn' / 'static_root'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static_cdn' / 'media_root'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'accounts:login'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- CKEditor ---
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['Maximize'],
        ],
        'height': 360,
        'width': '100%',
        'language': 'fa',
        'contentsLangDirection': 'rtl',
        'extraPlugins': ','.join(['justify', 'font', 'colorbutton']),
    },
    'body_en': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Format'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Image', 'Table'],
            ['Maximize'],
        ],
        'height': 360,
        'width': '100%',
        'language': 'en',
        'contentsLangDirection': 'ltr',
    },
}
