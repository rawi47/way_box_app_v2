import os
from utils.ftp import FtpUtils
from utils.cmd import Cmd
from utils.httpHandler import HttpHandler
from env_config.models import Env
from user.models import User
from . import run
import json
from django.conf import settings
lst = []
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'way_box_app_v2.settings')

def _initiate():
	print("############################ Starting main program #############################")
	run._config_main_prog()
	run._run_main_prog()
