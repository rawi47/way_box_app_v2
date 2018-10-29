"""
WSGI config for way_box_app_v2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from . import run

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'way_box_app_v2.settings')
try:
    run._config_main_prog()
    run._run_main_prog()
except Exception as e:
    print(str(e))
application = get_wsgi_application()
