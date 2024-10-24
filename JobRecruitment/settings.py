"""
Django settings for JobRecruitment project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os

os.path.join(os.path.dirname(__file__), '../templates').replace('\\', '/')
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ddt_33p8(2$8#y3f@7p1@df9flgshx0@rfp1hspph8mm8)dyce"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    'mdeditor',
    'widget_tweaks',

    # My app
    'UserAuth',
    'UserInfo',
    'PublishPosition',
    'Forum',
    'Application',
    'UserMessage',
    'PrivateMessage',
    'ContentReview'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # My middleware
    "UserAuth.middlewares.CheckLoginState.CheckLoginStateMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'ContentReview.middleware.SensitiveWordsMiddleware',
]

X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "JobRecruitment.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "JobRecruitment.wsgi.application"

# /JobRecruitment/local_settings.py
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobrecruitment',  # 数据库名字
        'USER': 'root',  #用户名
        'PASSWORD': '123456', #用户密码
        'HOST': '127.0.0.1',  # MySQL 在哪个 ip
        'PORT': '3306',  # 端口号
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'
USE_TZ = True

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_DIRS = [
    # 全局目录下的静态文件
    BASE_DIR / "static",
]
PROFILE_ROOT = os.path.join(BASE_DIR, 'static/images/')
RESUME_ROOT = os.path.join(BASE_DIR, 'resumes/')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

try:
    from .local_settings import *
except ImportError:  # 捕获导入异常
    pass

EMAIL_HOST = "smtp.sjtu.edu.cn"
EMAIL_PORT = 25 
EMAIL_HOST_USER = ""     # JAccount账号，不带邮箱后缀
EMAIL_HOST_PASSWORD = ""     # JAccount密码
EMAIL_USE_TLS = True 
EMAIL_FROM = "guoyu_1@sjtu.edu.cn"  # JAccount邮箱地址
EMAIL_TITLE = '邮箱激活'
