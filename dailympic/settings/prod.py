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

DEBUG = False

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),
]
