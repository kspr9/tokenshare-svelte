from dotenv import load_dotenv
import os
load_dotenv()

# for enabling auth
from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = reverse_lazy("tokenshare")
LOGOUT_REDIRECT_URL = reverse_lazy("login")

"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.7.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG can be True/False or 1/0
DEBUG = int(os.environ.get('DEBUG', default=1))

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "core.tokenshare",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

'''
    When you're ready to deploy, you'll run 'python manage.py collectstatic', 
    and Django will copy the static files from 'core/static' 
    (and any other app-specific 'static' directories) into 'core/staticfiles'. 
    Then, in your production environment, you'd configure your web server to serve the files from core/staticfiles.
'''
STATIC_ROOT = os.path.join(BASE_DIR, "core", "staticfiles")
STATIC_URL = "/static/"
# this is from https://dev.to/besil/my-django-svelte-setup-for-fullstack-development-3an8
STATICFILES_DIRS = (os.path.join(BASE_DIR, "core", "static"),)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

## For django-svelte conf
# this is from https://github.com/thismatters/django-svelte
#STATICFILES_DIRS = [
#    BASE_DIR.parent / "svelte" / "public" / "build",
#]




## Logging conf

'''
The log levels are:
    DEBUG: Low-level system information
    INFO: General system information
    WARNING: Minor problems related information
    ERROR: Major problems related information
    CRITICAL: Critical problems related information
'''

logging_level = (
    "INFO" if "LOGGING_LEVEL" not in os.environ else os.environ["LOGGING_LEVEL"]
)



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(asctime)s][%(levelname)8s][%(name)16.16s]@[%(lineno)5s]$ %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
        "propagate": False,
    },
    "loggers": {
        "django.server": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        "core": {
            "level": logging_level,
            "handlers": ["console"],
            "propagate": False,
        },
    },
}