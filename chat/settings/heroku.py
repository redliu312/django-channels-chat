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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())