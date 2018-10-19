from django.db import models
import subprocess
import datetime
import shlex

class Cmd(models.Model):


	def run(self,command,user,lst,printLog=True,getDate=True,shell=False):
		sudo_password = user.password
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
			popen = subprocess.call(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE,shell=shell)
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

	def _create_file_conf(source,content,right):
		file = open(source,right) 
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







