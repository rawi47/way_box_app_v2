import os
from utils.ftp import FtpUtils
from utils.cmd import Cmd
from utils.httpHandler import HttpHandler
from env_config.models import EnvSerializer,Env,SettingApp,InstalledSoftwares


from user.models import User
import json
from django.conf import settings
import  _thread, time,threading
import datetime


lst = []
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'way_box_app_v2.settings')

cmd = Cmd()
user_obj = User.objects.order_by('id')[0]
setting_app_obj = SettingApp.objects.order_by('sequence')
static_path = settings.STATICFILES_DIRS[0] + "/config/"

def _run_main_prog():
	getD = str(datetime.datetime.now()) + " - "
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
			try:
				httpHandler = HttpHandler()
				res = httpHandler._catch_all(url,data,params,headers,method)
					
				res_obj = json.loads(res[0])
				name = res_obj['name']
				if env_obj.name != name:
					Env.objects.filter(pk=env_obj.id).update(name=name)
				lst.append(getD + name)
			except Exception as e:
				lst.append(getD + str(e))

		commands = []
		for line in setting_app_obj:
			if line.api_mode in [app_mode, "commun"]:
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
				commands.append((cmmd,line.command_type,line.active))
				if len(cmmd_next) > 2:
					commands.append((cmmd_next,line.command_type_next,line.active))
				
				Cmd._create_file_conf(source,content,"w")		
	
		for line in commands:

			if line[2]:
				print(line[0])
				# run thread from install class
				try:
					
					if line[1] == "cmd":
						t = _thread.start_new_thread( cmd.run, (line[0],user_obj,lst,) )
					else:
						src = static_path + 'temp.sh'
						Cmd._create_file(src,line[0],"w")
						t = _thread.start_new_thread( cmd.run, ("chmod +x " + src,user_obj,lst,) )
						t = _thread.start_new_thread( cmd.run_sh, (src,user_obj,lst,) )

					
				except Exception as e:
					print("Python exception : " + str(e))

		for line in lst:
			print(line)
		
	except Exception as e:
		lst.append(getD + str(e))
	return lst
