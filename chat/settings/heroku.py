# should use postgres for heroku
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgres',
        'NAME': 'chat',
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {
        }
    }
}

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())



MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]