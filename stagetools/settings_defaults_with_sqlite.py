# noinspection PyUnresolvedReferences
from stagetools.settings_defaults import *

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': SYSTEM.database_sqlite_path,
    }
}
