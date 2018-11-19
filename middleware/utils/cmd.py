from django.db import models
import subprocess
import shlex
import os
from shutil import copy2
import fileinput
import requests
import logging

log = logging.getLogger(__name__)


class Cmd(models.Model):

	def run(self, command, user, lst=[]):
		sudo_password = user.password
		command = command.split()
		try:
			cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
			popen = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
			while True:
				line = popen.stdout.readline()
				line_err = popen.stderr.readline()

				if len(line) > 0:
					lst.append(line.decode().strip())
				elif len(line_err) > 0:
					lst.append(line_err.decode().strip())
				else:
					break

			popen.wait()

		except Exception as e:
			log.error("OSError > " + str(e))
			lst.append("OSError > " + str(e))

	def run_sh(self, command, user):
		sudo_password = user.password
		command = shlex.split(command)
		try:
			cmd1 = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
			popen = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
			while True:
				line = popen.stdout.readline()
				line_err = popen.stderr.readline()

				if len(line) > 0:
					log.error(line.decode().strip())
				elif len(line_err) > 0:
					log.error(line_err.decode().strip())
				else:
					break

			popen.wait()

		except Exception as e:
			log.error("OSError sh> " + str(e))

	def _create_dir(self, directory):
		if not os.path.exists(directory):
			os.makedirs(directory)

	def _copy_file(self, source, dst):
		copy2(source, dst)

	def _edit_files(self, filename, text_to_search, replacement_text):
		with fileinput.FileInput(filename, inplace=True) as file:
			for line in file:
				print(line.replace(text_to_search, replacement_text), end='')

	def _systemctl_status(self, pkg, user, lst):
		cmd = "systemctl status " + pkg
		self.run(cmd, user, lst)

	def _ndsctl_status(self, user, lst):
		cmd = "ndsctl status"
		self.run(cmd, user, lst)

	def _is_connected(self, hostname):
		try:
			resp = requests.get(hostname)
			return True, resp.status_code
		except Exception:
			return False, 500
