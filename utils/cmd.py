from django.db import models
import subprocess
import datetime


class Cmd(models.Model):


	def run(cmd,user,lst):
		sudo_password = user.password
		command = cmd
		command = command.split()

		count = 0
		try:
			cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
			popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)


			while True:
				line = popen.stdout.readline()

				if len(line) > 0:
					#the real code does filtering here
					lst.append(str(datetime.datetime.now()) + " - " + line.decode().strip() )
					count += 1
				else:
					break
			
			popen.wait()


		except Exception as e:
		    print ("OSError > " + str(e))
		except:
		    print ("Error > ")

		
		return

	def _create_file(source,content,right):
		file = open(source,right) 
		for line in content:
			file.write(line + "\n") 
		file.close() 

	def _create_hostapd(source,content,right,hostapd_obj):
		file = open(source,right) 
		file.write("interface=" + hostapd_obj.interface + "\n") 
		file.write("ssid=" + hostapd_obj.ssid+ "\n") 
		file.write("hw_mode=" + hostapd_obj.hw_mode+ "\n") 
		file.write("channel=" + hostapd_obj.channel+ "\n") 
		file.write("driver=nl80211\n") 
		file.write("macaddr_acl=" + hostapd_obj.macaddr_acl) 

	def _create_dnsmasq(source,content,right,dnsmasq_obj):
		file = open(source,right) 
		file.write("interface=" + dnsmasq_obj.interface + "\n") 
		file.write("listen-address=" + dnsmasq_obj.listen_address+ "\n") 
		file.write("bind-interfaces" + "\n") 
		file.write("server=" + dnsmasq_obj.server+ "\n") 
		file.write("domain-needed\n") 
		file.write("bogus-priv\n") 
		file.write("dhcp-range=" + dnsmasq_obj.dhcp_range + "\n") 
		file.write("address=" + dnsmasq_obj.address + "\n") 
		file.write("ipset=" + dnsmasq_obj.ipset) 


