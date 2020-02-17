
from .base import *
import os

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      'settings.dev')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


