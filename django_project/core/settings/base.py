import dj_database_url
import os
from core.settings.env import ENV_BOOL, ENV_STR, ENV_LIST, ABS_PATH, PARDIR, ENV_NUM

# default value is False
DEBUG = ENV_BOOL('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_STR('SECRET_KEY')

ALLOWED_HOSTS = ENV_LIST('ALLOWED_HOSTS', ',', ['*'] if DEBUG else [])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'channels',
    'rest_framework',
    'rest_framework_gis',
    'gps_tracking_app',
    'rest_framework_swagger',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


TEMPLATE_DIR = os.path.join(PARDIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Databases
DATABASES = {'default': dj_database_url.config()}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Zagreb'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Django-Rest-Framework settings
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

# Django-Channels settings
ASGI_APPLICATION = 'core.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', ENV_NUM('REDIS_PORT', 6379))],
        },
    },
}


# CORS
CORS_ORIGIN_WHITELIST = ENV_LIST('CORS_ORIGIN_WHITELIST', ',')

# Openlayer
OPENLAYERS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'

STATIC_URL = '/static/'
STATIC_ROOT = ABS_PATH(PARDIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(PARDIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = ABS_PATH(PARDIR, 'media')

# Log dir path
LOG_DIR = ABS_PATH(PARDIR, 'logs')

MQTT_TTN = {
    'broker_address': ENV_STR('MQTT_BROKER_ADDRESS'),
    'port': ENV_NUM('MQTT_PORT'),
    'user': ENV_STR('MQTT_USER'),
    'password': ENV_STR('MQTT_PASSWORD'),
    'device': ENV_STR('MQTT_DEVICE'),
    'device2': ENV_STR('MQTT_DEVICE2')
}
