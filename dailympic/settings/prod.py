# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

import os
from .base import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings.prod')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secrets['PROD_MYSQL_NAME'],
        'USER': secrets['PROD_MYSQL_USER'],
        'PASSWORD': secrets['PROD_MYSQL_PASSWORD'],
        'HOST': secrets['PROD_MYSQL_HOST'],
        'PORT': '3306',
    }
}

DEBUG = True

#S3 settings
DEFAULT_FILE_STORAGE = 'dailympic.storages.MediaStorage'
STATICFILES_STORAGE = 'dailympic.storages.StaticStorage'
MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'

AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
