from os import path
from utils.ftp import FtpUtils
from utils.cmd import Cmd
from utils.httpHandler import HttpHandler
from env_config.models import EnvSerializer,Env,SettingApp,InstalledSoftwares



from user.models import User
import json
from django.conf import settings
import  _thread, time,threading
import datetime

cmd = Cmd()
httpHandler = HttpHandler()

def _config_main_prog():
	lst = []
	user_obj = User.objects.order_by('id')[0]
	setting_app_obj = SettingApp.objects.order_by('sequence')
	env_obj = Env.objects.order_by('api_key')[0]
	app_mode = env_obj.api_mode

	static_path = path.join(env_obj.root_dir,env_obj.app_dir,env_obj.config_dir)
	getD = str(datetime.datetime.now()) + " - "
	try:
		commands = []
		for line in setting_app_obj:
			if line.api_mode in [app_mode, "commun"]:

				source = path.join(static_path , line.origine)
				if len(line.directory) > 2:
					dir = path.join(static_path,line.directory);
					cmd._create_dir(dir)
					source = path.join(dir , line.origine)

				if len(line.sub_directory) > 2:
					dir = path.join(static_path,line.directory,line.sub_directory);
					cmd._create_dir(dir)
					source = path.join(dir , line.origine)
					
				content = line.params
				args = [source,line.dest]
				cmmd = line.cmd

				i = 0
				for arg in args:
					cmmd = cmmd.replace("arg" + str(i), arg)
					i += 1
				if len(cmmd) > 2:
					commands.append((cmmd,line.command_type,line.active))


				cmd._create_file_conf(source,content,"w")


		for line in commands:

			if line[2]:
				lst.append(line[0])
				# run thread from install class
				try:

					if line[1] == "cmd":
						cmd.run(line[0],user_obj,lst)
					else:
						src = static_path + 'temp.sh'
						Cmd._create_file(src,line[0],"w")
						cmd.run("chmod +x " + src,user_obj,lst)
						cmd.run_sh(src,user_obj,lst)
						cmd.run("rm -rf " + src,user_obj,lst)


				except Exception as e:
					print("Python exception : " + str(e))

		for line in lst:
			print(line)

	except Exception as e:
		lst.append(getD + str(e))
	return lst

def _run_main_prog():
	lst = []
	user_obj = User.objects.order_by('id')[0]
	setting_app_obj = SettingApp.objects.order_by('sequence')
	env_obj = Env.objects.order_by('api_key')[0]

	static_path = path.join(env_obj.root_dir,env_obj.app_dir,env_obj.config_dir)

	getD = str(datetime.datetime.now()) + " - "

	app_mode = env_obj.api_mode
	API_HOST = env_obj.api_host
	API_KEY = env_obj.api_key
	API_SECRET = env_obj.api_secret
	try:

		if app_mode == "wlan":
			httpHandler._set_establichement_name(API_HOST,API_KEY,API_SECRET,lst)

		commands = []
		for line in setting_app_obj:
			if line.api_mode in [app_mode, "commun"]:
				source = static_path + line.origine
				content = line.params
				args = [source,line.dest]
				cmmd_next = line.cmd_next
				i = 0
				for arg in args:
					cmmd_next = cmmd_next.replace("arg" + str(i), arg)
					i += 1
				if len(cmmd_next) > 2:
					commands.append((cmmd_next,line.command_type_next,line.active))


		for line in commands:
			if line[2]:
				lst.append(line[0])
				try:
					if line[1] == "cmd":
						cmd.run(line[0],user_obj,lst)
					else:
						src = static_path + 'temp.sh'
						Cmd._create_file(src,line[0],"w")
						cmd.run("chmod +x " + src,user_obj,lst)
						cmd.run_sh(src,user_obj,lst)
						cmd.run("rm -rf " + src,user_obj,lst)

				except Exception as e:
					print("Python exception : " + str(e))

		for line in lst:
			print(line)

	except Exception as e:
		lst.append(getD + str(e))
	return lst
