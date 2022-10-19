#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
ENVIRONMENT = os.environ.get('ENVIRONMENT', default='local')
# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'production':
    SECRET_KEY = os.environ.get('SECRET_KEY')
else:
    SECRET_KEY = '56gfdf062)+wellq8no=#kq2&=x+_^07i3cs0=qh1vd&s%$321'

ALLOWED_HOSTS = ["*"]


# Application definition
LOCAL_APPS = [
    'core',
    'customer',
    'dashboard',
    'item',
    'talk',
]
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
]
THIRD_PARTY_APPS = [        
    'escapejson',
    'corsheaders',
    'crispy_forms',    
    'django.contrib.sites',
    'allauth',
    'allauth.account',    
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rules.apps.AutodiscoverRulesConfig',
    'simple_history',
]
INSTALLED_APPS = LOCAL_APPS + DJANGO_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

# Authorization
AUTH_USER_MODEL = 'dashboard.User'

AUTHENTICATION_BACKENDS = [
    #'config.backends.AuthBackend'
    'allauth.account.auth_backends.AuthenticationBackend'
]

ROOT_URLCONF = 'config.urls'

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
            'libraries' : {
                'staticfiles': 'django.templatetags.static', 
                'search_highlight': 'dashboard.templatetags.search_highlight',
                'notification_template': 'dashboard.templatetags.notification_template',
                'item_template': 'dashboard.templatetags.item_template',
                'core_template': 'dashboard.templatetags.core_template'
            }
            
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
#ASGI_APPLICATION = 'config.asgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if ENVIRONMENT == 'local':
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env/')]

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

    BACKEND_URL="http://localhost:8000"
    #SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    FRONT_END_URL = "http://localhost:8000"
    
    PRODUCTION = False
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


if ENVIRONMENT == 'production':
    PRODUCTION = True
    DEBUG = False
    ALLOWED_HOSTS = ['*']

    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('RDS_DB_NAME'),
            'USER': os.environ.get('RDS_USERNAME'),
            'PASSWORD': os.environ.get('RDS_PASSWORD'),
            'HOST': os.environ.get('RDS_HOSTNAME'),
            'PORT': os.environ.get('RDS_PORT', default=3306),
            'OPTIONS': {
                'charset': 'utf8mb4'  # This is the important line
            }
        }
    }

    if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_STORAGE_BUCKET_NAME" in os.environ:
        AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
        AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
        AWS_DEFAULT_ACL = None
        AWS_QUERYSTRING_AUTH = False
        AWS_S3_SIGNATURE_VERSION = 's3v4'
        AWS_S3_REGION_NAME = "ap-northeast-1"
        AWS_S3_ENCRYPTION = True
        AWS_S3_HOST = ''
        AWS_IS_GZIPPED = True
        AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
        }
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        STATIC_URL = os.environ.get(
            'STATIC_URL', default=f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/')
        MEDIA_URL = os.environ.get(
            'MEDIA_URL', default=f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/')
        HOST_NAME = 'https://shapel-medicine.com'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'django_cache',        
    }
}
ACCESS_TOKEN_PREFIX = 'ACCESS_TOKEN'
CACHE_TTL = 60 * 60 * 24 * 3

from datetime import timedelta

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'email_log'
EMAIL_FROM = "hello@hello.io"
NAME_FROM = "Hello"
EMAIL_USE_TLS = True

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'SCOPE': [
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email'
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    }
}

SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

CALLBACK_URL_YOU_SET_ON_GOOGLE='http://127.0.0.1:8000/api/account/google/callback/'
