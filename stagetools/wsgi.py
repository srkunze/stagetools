"""
WSGI config for stagetools project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

# noinspection PyUnresolvedReferences
import aaa_env_setup
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
