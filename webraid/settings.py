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


# Application definition

INSTALLED_APPS = (
    'utils',
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
                 os.path.join(BASE_DIR, 'templates/forum')]
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


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

<<<<<<< HEAD
=======
# 4 - Static and media storage
>>>>>>> 9350566dfec21f0cd1aad032f264d82b996d8fba

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    'static/',
)

# Media files
MEDIA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/media/"
MEDIA_URL = 'media/'

# Login and authenticaiton
LOGIN_REDIRECT_URL = '/users'
LOGOUT_REDIRECT_URL = '/login'
LOGIN_URL = '/login'

LOGIN_REQUIRED_URLS = (
    r'/forum/(.*)$',
    r'/users/(.*)$',
)

LOGIN_EXEMPT_URLS = (
    r'^home/$',
)

# Django-countries settings
COUNTRIES_FIRST = [
    'FR',
    'UK',
    'US',
]

COUNTRIES_FIRST_REPEAT = True
