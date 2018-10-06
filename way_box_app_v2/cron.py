import os
from utils.ftp import FtpUtils
from utils.cmd import Cmd
from utils.httpHandler import HttpHandler
from env_config.models import Env
from env_config.models import Hostapd
from env_config.models import Dnsmasq
from env_config.models import Hosts
from env_config.models import Ipset
from env_config.models import IpTables
from env_config.models import Interfaces
from env_config.models import Nodogsplash
from user.models import User
import json
from django.conf import settings
import configparser 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'way_box_app_v2.settings')

def _initiate():
	try:
		lst = []
		user_obj = User.objects.order_by('id')[0]
		env_obj = Env.objects.order_by('api_key')[0]
		hostapd_obj = Hostapd.objects.order_by('id')[0]
		dnsmasq_obj = Dnsmasq.objects.order_by('id')[0]
		hosts_obj = Hosts.objects.order_by('id')[0]
		ipset_obj = Ipset.objects.order_by('id')[0]
		iptables_obj = IpTables.objects.order_by('id')[0]
		interfaces_obj = Interfaces.objects.order_by('id')[0]
		nodogsplash_obj = Nodogsplash.objects.order_by('id')[0]

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

			hostapd_source = settings.STATICFILES_DIRS[0] + "/config/hostapd/hostapd.conf"
			dnsmas_source = settings.STATICFILES_DIRS[0] + "/config/dnsmasq." + app_mode + ".conf"
			hosts_source = settings.STATICFILES_DIRS[0] + "/config/hosts"
			ipset_source = settings.STATICFILES_DIRS[0] + "/config/ipset.ipv4.nat"
			iptables_source = settings.STATICFILES_DIRS[0] + "/config/iptables." + app_mode + ".ipv4.nat"
			interfaces_source = settings.STATICFILES_DIRS[0] + "/config/network/interfaces." + app_mode
			nodogsplash_source = settings.STATICFILES_DIRS[0] + "/config/nodogsplash/nodogsplash." + app_mode + ".conf"


			Cmd._create_hostapd(hostapd_source,[],"w",hostapd_obj)
			Cmd._create_dnsmasq(dnsmas_source,[],"w",dnsmasq_obj)
			Cmd._create_file(hosts_source,[hosts_obj.params],"w")
			Cmd._create_file(ipset_source,[ipset_obj.params],"w")	
			Cmd._create_file(interfaces_source,[interfaces_obj.params],"w")
			Cmd._create_file(nodogsplash_source,[nodogsplash_obj.params],"w")

			commands = []
			cmd_ipset = "ipset --restore < " + ipset_obj.dest
			commands.append(cmd_ipset)

			cmd_iptables = "iptables-restore < " + iptables_obj.dest
			commands.append(cmd_iptables)

			cmd_dns = "ln -sf " + dnsmas_source + " " + dnsmasq_obj.dest
			commands.append(cmd_dns)

			cmdn_iptables = "ln -sf " + iptables_source + " " + iptables_obj.dest
			commands.append(cmdn_iptables)

			cmdn_interfaces = "ln -sf " + interfaces_source + " " + interfaces_obj.dest
			commands.append(cmdn_interfaces)

			cmdn_nodogsplash = "ln -sf " + nodogsplash_source + " " + nodogsplash_obj.dest
			commands.append(cmdn_nodogsplash)

			cmd_hosts = "ln -sf " + hosts_source + " " + hosts_obj.dest
			commands.append(cmd_hosts)


			cmd_hostapd = "cp -rf " + hostapd_source + " " + hostapd_obj.dest
			commands.append(cmd_hostapd)

			cmd_exec_nodogsplash = "nodogsplash"
			commands.append(cmd_exec_nodogsplash)
		


			cmd_forward = "sysctl -w net.ipv4.ip_forward=1"
			commands.append(cmd_forward)

			command = "hostapd -B " + hostapd_obj.dest	
			commands.append(command)
			for line in commands:
				print(line)
				if not settings.DEBUG:
					Cmd.run(command,user_obj,lst)

			for line in lst:
				print(line)
	except Exception as e:
		print(str(e))

