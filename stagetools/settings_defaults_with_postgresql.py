# noinspection PyUnresolvedReferences
from stagetools.settings_defaults import *

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SYSTEM.database_name,
    }
}
