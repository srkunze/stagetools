from aaa_env_setup import SYSTEM

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SYSTEM.is_debug

ROOT_URLCONF = SYSTEM.django_rooturls
WSGI_APPLICATION = SYSTEM.django_wsgi_application

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = SYSTEM.static_url
STATIC_ROOT = SYSTEM.static_dir

MEDIA_URL = SYSTEM.media_url
MEDIA_ROOT = SYSTEM.media_dir
