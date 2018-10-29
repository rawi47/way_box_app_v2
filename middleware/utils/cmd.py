from django.db import models
import subprocess
import datetime
import shlex
from django.http import HttpResponse
from env_config.models import Env
import configparser

class Cmd(models.Model):


	def run(self,command,user,lst,printLog=True,getDate=True,shell=False):
		sudo_password = user.password
		#lst.append(command)
		command = command.split()
		try:
			cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
			popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE,shell=shell)
			while True:
				line = popen.stdout.readline()

				if len(line) > 0:
					getD = ""
					if getDate:
						getD = str(datetime.datetime.now()) + " - "
					lst.append(getD + line.decode().strip() )
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
			popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE,shell=shell)
			while True:
				line = popen.stdout.readline()

				if len(line) > 0:
					getD = ""
					if getDate:
						getD = str(datetime.datetime.now()) + " - "
					lst.append(getD + line.decode().strip() )
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

		self._change_configuration(source)

		for line in content.splitlines():

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

	def _change_configuration(self,filename):
		config = configparser.ConfigParser()
		config.read(filename)
		print(config)
		#
		#
		# with open(filename, 'wb') as handle:
		#     cp.write(handle)
