from django.db import models
import subprocess
import datetime


class Cmd(models.Model):


	def run(cmd,user,lst,printLog=True):
		sudo_password = user.password
		command = cmd
		command = command.split()
		try:
			cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
			popen = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)


			while True:
				line = popen.stdout.readline()

				if len(line) > 0:
					#the real code does filtering here

					lst.append(str(datetime.datetime.now()) + " - " + line.decode().strip() )
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
		file.write(content) 
		file.close() 




