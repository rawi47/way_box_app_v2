import os
from utils.ftp import FtpUtils
from utils.cmd import Cmd
from utils.httpHandler import HttpHandler
from env_config.models import EnvSerializer,Env,SettingApp,InstalledSoftwares


from user.models import User
import json
from django.conf import settings
import subprocess
import shlex

lst = []
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'way_box_app_v2.settings')

cmd = Cmd()
user_obj = User.objects.order_by('id')[0]
setting_app_obj = SettingApp.objects.order_by('sequence')
static_path = settings.STATICFILES_DIRS[0] + "/config/"

def _run_main_prog():
	try:
		
		user_obj = User.objects.order_by('id')[0]
		env_obj = Env.objects.order_by('api_key')[0]
			

		app_mode = env_obj.api_mode
		httpHandler = HttpHandler()

		if app_mode == "wlan":
			API_HOST = env_obj.api_host
			API_KEY = env_obj.api_key
			API_SECRET = env_obj.api_secret

			path = "/customers/establishment"
			url = "http://" + API_HOST + path
			method = "GET"

			data = {}
			params = {}
			signature = httpHandler._sign(API_KEY, API_SECRET, params)
			headers = {}
			headers['Host'] = API_HOST
			headers['X-API-Key'] = API_KEY
			headers['X-API-Sign'] = signature
			httpHandler = HttpHandler()
			res = httpHandler._catch_all(url,data,params,headers,method)
				
			res_obj = json.loads(res[0])
			name = res_obj['name']
			if env_obj.name != name:
				Env.objects.filter(pk=env_obj.id).update(name=name)

		commands = []
		for line in setting_app_obj:
			if line.api_mode in [app_mode, "commun"] :
				source = static_path + line.origine
				content = line.params
				args = [source,line.dest]
				cmmd = line.cmd
				cmmd_next = line.cmd_next

				i = 0
				for arg in args:
					cmmd = cmmd.replace("arg" + str(i), arg)
					cmmd_next = cmmd_next.replace("arg" + str(i), arg)
					i += 1
				commands.append(cmmd)
				if len(cmmd_next) > 2:
					commands.append(cmmd_next)
				
				Cmd._create_file(source,content,"w")		

		for line in commands:
			print(line)
			shell = False
			cm = "sudo " + static_path + './test.sh param1 param2'
			#subprocess.call(shlex.split(cm))
			cmd.run(line,user_obj,lst,shell=shell)

		for line in lst:
			print(line)
	except Exception as e:
		print(str(e))
