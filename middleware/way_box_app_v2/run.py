from os import path,walk
from utils.ftp import FtpUtils
from utils.cmd import Cmd
from utils.webFunctions import Httphandler
from env_config.models import EnvSerializer,Env



from user.models import User
import json
from django.conf import settings
import  _thread, time,threading
import datetime
import logging
log = logging.getLogger(__name__)

cmd = Cmd()
webFunctions = Httphandler()

def _config_main_prog():

	lst = []
	user_obj = User.objects.order_by('id')[0]
	env_obj = Env.objects.order_by('api_key')[0]
	if not env_obj.run_on_start:
		return
	app_mode = env_obj.api_mode
	static_path = path.join(env_obj.root_dir,env_obj.app_dir,env_obj.config_dir)
	origin_path = path.join(env_obj.root_dir,env_obj.app_dir,env_obj.origin_config_dir)
	getD = str(datetime.datetime.now()) + " - "
	interface = "eth1"
	ssid = env_obj.name.upper() + env_obj.ssid_prefix

	etc_dir = env_obj.etc_dir
	portal = env_obj.portal_url
	do_hostapd = True

	try:
		files =[
			("ipset.ipv4.nat",True),
			("iptables.ipv4.nat",True),
			("dnsmasq.conf",True),
			("dhcpcd.conf",True),
			("nodogsplash/nodogsplash.conf",True),
			("nodogsplash/htdocs/splash.html",True),
			("hostapd/hostapd.conf",do_hostapd),
			("hostapd/hostapd",do_hostapd)
		]
		directories = ["nodogsplash","nodogsplash/htdocs","hostapd"]
		for dr in directories:
			dir = path.join(static_path,dr)
			cmd._create_dir(dir)


		for fl,ln in files:
			source = path.join(origin_path,fl)
			dest = path.join(static_path,fl)
			cmd._copy_file(source,dest)

			cmd._edit_files(dest,"arg0",interface)
			cmd._edit_files(dest,"arg1",ssid)
			cmd._edit_files(dest,"arg2",portal)
			config_dst = path.join(etc_dir,fl)
			if ln:

				command = "ln -sf " + dest + " " + config_dst
				lst.append(command)
				cmd.run(command,user_obj,lst)

	except Exception as e:
		lst.append(getD + str(e))
		log.error(str(e))
	return lst

def _run_main_prog():
	getD = str(datetime.datetime.now()) + " - "
	lst = []
	user_obj = User.objects.order_by('id')[0]
	env_obj = Env.objects.order_by('api_key')[0]
	if not env_obj.run_on_start:
		return
	app_mode = env_obj.api_mode
	static_path = path.join(env_obj.root_dir,env_obj.app_dir,env_obj.config_dir)


	commands_sh = [
		"ipset --restore < /etc/ipset.ipv4.nat",
		"iptables-restore < /etc/iptables.ipv4.nat"
	]

	commands = []


	commands.append("nodogsplash")


	for cmd_sh in commands_sh:
		log.error(cmd_sh)
		lst.append(cmd_sh)
		src = static_path + 'temp.sh'
		Cmd._create_file(src,cmd_sh,"w")
		cmd.run("chmod +x " + src,user_obj,lst)
		cmd.run_sh(src,user_obj,lst)
		cmd.run("rm -rf " + src,user_obj,lst)



	for cmmd in commands:
		log.error(cmmd)
		lst.append(cmmd)
		cmd.run(cmmd,user_obj,lst)



	return lst
