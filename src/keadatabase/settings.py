"""
Django settings for keadatabase project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'DO_NOT_USE_IN_PRODUCTION'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Production settings for security and geo libraries
if os.environ.get('IS_PRODUCTION') == 'True' \
   and 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

    DEBUG = False

    ALLOWED_HOSTS = [
        '.keadatabase.nz'
    ]

    GEOS_LIBRARY_PATH = "{}/libgeos_c.so".format(os.environ.get('GEO_LIBRARIES_PATH'))
    GDAL_LIBRARY_PATH = "{}/libgdal.so".format(os.environ.get('GEO_LIBRARIES_PATH'))
    PROJ4_LIBRARY_PATH = "{}/libproj.so".format(os.environ.get('GEO_LIBRARIES_PATH'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'theme',
    'django.contrib.admin',

    'storages',
    'versatileimagefield',
    'django_filters',
    'corsheaders',
    'rest_framework',
    'rest_framework_gis',
    'debug_toolbar',

    'birds',
    'bands',
    'locations',
    'synchronise',
    'sightings',
    'report',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'keadatabase.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'keadatabase.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

import dj_database_url

DATABASES = {}

DATABASES['default'] = dj_database_url.config(
    default='postgres://postgres:@localhost:5432/keadatabase',
    conn_max_age=600
    )

DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-nz'

TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'PAGE_SIZE': 72
}


# CORS

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
)

if not DEBUG:
    CORS_ORIGIN_WHITELIST = (
        'beta.keadatabase.nz',
        'www.keadatabase.nz',
        'keadatabase.nz',
    )


if os.environ.get('CORS_ALLOW_LOCALHOST') == 'True':
    CORS_ORIGIN_WHITELIST += (
        'localhost:3000',
    )


# Custom admin site header

ADMIN_SITE_HEADER = "Kea Database API"
ADMIN_SITE_TITLE = "Kea Database API"
ADMIN_INDEX_TITLE = "Administration"


# Production security

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'


# Amazon S3 storage

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
    AWS_LOCATION = '/media'
    AWS_IS_GZIPPED = True


# Versatile Image Field

VERSATILEIMAGEFIELD_SETTINGS = {
    'create_images_on_demand': False,
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'profile_picture': [
        ('full_size', 'url'),
        ('thumbnail', 'crop__350x250'),
        ('large', 'crop__500x500'),
    ],
}


# Debug toolbar

if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']
