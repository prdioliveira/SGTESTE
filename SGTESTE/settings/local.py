import sys
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sgteste',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

INSTALLED_APPS += [
    'app.sgteste_app',
]

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_USE_SSL = True
EMAIL_PORT = os.environ.get('EMAIL_PORT')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },

    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/sgteste.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django_request.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'default'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}