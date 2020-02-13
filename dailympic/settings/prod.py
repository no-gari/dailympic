# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

import os
from .base import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings.prod')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}
