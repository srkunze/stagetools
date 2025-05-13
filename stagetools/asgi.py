"""
ASGI config for stagetools project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""

import importlib

# noinspection PyUnresolvedReferences
from aaa_env_setup import SYSTEM

try:
    websocket_module = importlib.import_module(SYSTEM.core_app + '.websocket')
except ImportError:
    websocket_module = None
try:
    lifespan_module = importlib.import_module(SYSTEM.core_app + '.lifespan')
except ImportError:
    lifespan_module = None
from django.core.asgi import get_asgi_application


async def application(scope, receive, send):
    if scope['type'] == 'http':
        # Let Django handle HTTP requests
        await get_asgi_application()(scope, receive, send)
    elif websocket_module and scope['type'] == 'websocket':
        await websocket_module.websocket_application(scope, receive, send)
    elif lifespan_module and scope['type'] == 'lifespan':
        await lifespan_module.lifespan_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
