"""
Django settings for aidoc project.
"""

import logging
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-e0l#g#nd9)(1n&364=+cg1z=v#3(u98s+-@ps97k!ge7$=ofe^"
)

DEBUG = os.environ.get("DEBUG") == "True"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "app", ".fly.dev"]
CSRF_TRUSTED_ORIGINS = ["https://*.fly.dev"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "rest_framework.authtoken",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "core",
]

# REST_FRAMEWORK = {
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.authentication.TokenAuthentication"
#     ]
# }

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
LOGIN_REDIRECT_URL = "/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "aidoc.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "aidoc.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    "default": dj_database_url.config(env="DATABASE_URL"),
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

STATICFILES_DIRS = (os.path.join(BASE_DIR, "aidoc/static_files"),)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "core.User"
LOGIN_URL = "login"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = os.environ.get("SERVER_EMAIL")

REDIS_URL = os.getenv("REDIS_URL")
CELERY_BROKER_URL = f"{REDIS_URL}/0"
CELERY_TIMEZONE = "America/Sao_Paulo"
CELERY_TASK_SERIALIZER = "pickle"
CELERY_ON = os.getenv("CELERY_ON", "True") in {
    "True",
    "true",
    "1",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
LOGGER = logging.getLogger(__name__)

LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")
VECTOR_DB = os.environ.get("VECTOR_DB", "supabase")

QDRANT_PATH = None
qpath = os.environ.get("QDRANT_PATH")
if qpath:
    QDRANT_PATH = os.path.join(BASE_DIR, qpath)
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_KEY = os.environ.get("QDRANT_KEY")

SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
