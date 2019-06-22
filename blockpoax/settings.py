import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'no&0=z4o8nszf3edrnj17g$he73i5y^rq$_51gouniuqohvtse'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    'public',
    'userauth',
    'dashboard',
    'telegram',
    'debug_toolbar',
]

sentry_sdk.init(
    dsn="https://8fe645d6071d45058d841bede9a9ba75@sentry.io/1482482",
    integrations=[DjangoIntegration()]
)

DEFAULT_FROM_EMAIL = "admin@smmpanel.guru"
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'home'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@smmpanel.guru'
EMAIL_HOST_PASSWORD = 'OrionNebula100!'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

CORS_ORIGIN_WHITELIST = [
    "https://coincap.io",
]

HTML_MINIFY = True

ROOT_URLCONF = 'blockpoax.urls'

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
    'LOCATION': '127.0.0.1:11211',
  },
  'staticfiles': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'staticfiles-filehashes'
  }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blockpoax.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smmpanel',
        'USER': 'smmpanel',
        'PASSWORD': 'alpha2beta',
        'HOST': 'localhost',
        'PORT': '',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/dist/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dist')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
