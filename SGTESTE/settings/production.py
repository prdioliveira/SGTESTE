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