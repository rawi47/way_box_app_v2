from django.db import models
import subprocess
import datetime
import shlex
from django.http import HttpResponse
from env_config.models import Env
import os
import socket
from shutil import copy2
from os import walk
import fileinput
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class Cmd(models.Model):


	def run(self,command,user,lst,printLog=True,getDate=True,shell=False):
		sudo_password = user.password
		#lst.append(command)
		command = command.split()
		try:
			cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
			popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell)
			while True:
				line = popen.stdout.readline()
				line_err = popen.stderr.readline()

				if len(line) > 0:
					getD = ""
					if getDate:
						getD = str(datetime.datetime.now()) + " - "
					lst.append(getD + line.decode().strip() )
				elif  len(line_err) > 0:
					getD = ""
					if getDate:
						getD = str(datetime.datetime.now()) + " - "
					lst.append(getD + line_err.decode().strip() )
				else:
					break

			popen.wait()

		except Exception as e:
		    lst.append ("OSError > " + str(e))
		except:
		    lst.append ("Error > ")

		return

	def run_sh(self,command,user,lst,printLog=True,getDate=True,shell=False):
		sudo_password = user.password
		command = shlex.split(command)
		try:
			cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
			popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell)
			while True:
				line = popen.stdout.readline()
				line_err = popen.stderr.readline()

				if len(line) > 0:
					getD = ""
					if getDate:
						getD = str(datetime.datetime.now()) + " - "
					lst.append(getD + line.decode().strip() )
				elif  len(line_err) > 0:
					getD = ""
					if getDate:
						getD = str(datetime.datetime.now()) + " - "
					lst.append(getD + line_err.decode().strip() )
				else:
					break

			popen.wait()

		except Exception as e:
		    lst.append ("OSError sh> " + str(e))
		except:
		    lst.append ("Error > ")

		return

	def _create_file_conf(self,source,content,right):
		file = open(source,right)
		env_obj = Env.objects.order_by('api_key')[0]
		for line in content.splitlines():
			if "WAY_BOX" in line:
				env_obj = Env.objects.order_by('api_key')[0]
				file.write("ssid=" + env_obj.name.upper() + env_obj.ssid_prefix + "\n")
			else:
				file.write(line + "\n")
		file.close()

	def _create_file(source,content,right):
		file = open(source,right)
		file.write(content)
		file.close()


	def _read_file(self,file,user,lst):
		cmds = []
		cmds.append("cat " + file)
		for line in cmds:
			self.run(line,user,lst,getDate=False)

		return lst

	def _create_dir(self,directory):
	    if not os.path.exists(directory):
	        os.makedirs(directory)

	def _copy_file(self,source,dst):
		copy2(source, dst)

	def _list_dir(self,mypath):
		f = []
		for (dirpath, dirnames, filenames) in walk(mypath):
		    f.extend(filenames)
		return f

	def _edit_files(self,filename,text_to_search,replacement_text):
		with fileinput.FileInput(filename, inplace=True) as file:
		    for line in file:
		        print(line.replace(text_to_search, replacement_text), end='')
	def _systemctl_status(self,pkg,user,lst):
		cmd = "systemctl status " + pkg
		self.run(cmd,user,lst,getDate=False)

		return lst

	def _ndsctl_status(self,user,lst):
		cmd = "ndsctl status"
		self.run(cmd,user,lst,getDate=False)

		return lst
	def _is_connected(self,hostname):
		try:
			session = requests.Session()
			retry = Retry(connect=3, backoff_factor=0.5)
			adapter = HTTPAdapter(max_retries=retry)
			session.mount('http://', adapter)
			session.mount('https://', adapter)

			resp = session.get(hostname)
			return True,resp.status_code
		except Exception as e:
			return False,str(e)
