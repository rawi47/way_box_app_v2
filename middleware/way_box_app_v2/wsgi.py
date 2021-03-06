"""
WSGI config for way_box_app_v2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
import os
import  _thread, time,threading

from django.core.wsgi import get_wsgi_application
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'way_box_app_v2.settings')
application = get_wsgi_application()
print("#############################################################################################")
import way_box_app_v2.run as rn



try:
    t = _thread.start_new_thread( rn._run_main_prog, () )
except Exception as e:
    print("Python exception : " + str(e))
