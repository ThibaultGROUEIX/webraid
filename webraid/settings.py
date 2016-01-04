"""
Django settings for webraid project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rc@nwvkk5_9dx$#j+#87egqqaa-y-08tp*b!#h+xy-&7*5sdl)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# ----------------------------
# 1 - Application definition
# 2 - Database
# 3 - Internationalization
# 4 - Static and media storage
# 5 - Login and authentication
# 6 - Django-countries settings
# 7 - Email settings
# ----------------------------

# 1 - Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django-countries app to manage countries
    'django_countries',
    'profiles',
    'forum',
    'notifications',
    'notification_manager',
    'utils'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'utils.snippets.login_required.RequireLoginMiddleware',
)

ROOT_URLCONF = 'webraid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates/profiles'),
                 os.path.join(BASE_DIR, 'templates/admin'),
                 os.path.join(BASE_DIR, 'templates/forum'),
                 os.path.join(BASE_DIR, "templates/email")]
        ,
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

WSGI_APPLICATION = 'webraid.wsgi.application'

# 2 - Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },

    'notifications': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'notifications')
    }
}
NOTIFICATION_DB = 'notifications'
DATABASES_ROUTERS = ['notifications.routers.NotificationRouter']

# 3 - Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# 4 - Static and media storage

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    'static/',
)

# Media files
MEDIA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/media/"
MEDIA_URL = 'media/'

# 5 - Login and authentication
LOGIN_REDIRECT_URL = '/home'
LOGOUT_REDIRECT_URL = '/login'
LOGIN_URL = '/login'

LOGIN_REQUIRED_URLS = (
    r'/forum/(.*)$',
    r'/users/(.*)$',
)

LOGIN_EXEMPT_URLS = ()

# 6 - Django-countries settings
COUNTRIES_FIRST = [
    'FR',
    'UK',
    'US',
]

COUNTRIES_FIRST_REPEAT = True

# 7 - Email settings
import json

smtp_settings_file = open(os.path.join(BASE_DIR, 'smtp_settings.json'))
smtp_settings = json.load(smtp_settings_file)

EMAIL_USE_TLS = True
EMAIL_HOST = smtp_settings['host']
EMAIL_PORT = smtp_settings['port']
EMAIL_HOST_USER = smtp_settings['host_user']
EMAIL_HOST_PASSWORD = smtp_settings['password']
