from django.db import models
from pathlib import Path


class Env(models.Model):


	def __str__(self):
		return self.name

	modes = (
		('wlan','wlan'),
		('eth','eth')
	)

	name = models.CharField(max_length=200,default="name")
	api_host = models.CharField(max_length=200,default="api.way-connect.com")
	api_key = models.CharField(max_length=200)
	api_secret = models.CharField(max_length=200)
	api_port = models.IntegerField(default=80) 
	
	root_dir = models.CharField(max_length=200,default=str(Path.home()))
	version = models.CharField(max_length=200,default="0.0.1")
	patch = models.CharField(max_length=200,default="0.0.1")
	app_dir = models.CharField(max_length=200,default="Way-Connect_Box")
	git_repo = models.CharField(max_length=200)

	ftp_host = models.CharField(max_length=200,default="127.0.0.1")
	ftp_user = models.CharField(max_length=200,default="user")
	ftp_password = models.CharField(max_length=200,default="password")

	ssid_prefix = models.CharField(max_length=200,default="_FREE_WIFI")


	api_mode = models.CharField(
	    max_length=200,
	    choices=modes,
	)


class Hostapd(models.Model):


	def __str__(self):
		return self.name

	name = models.CharField(max_length=200,default="")
	params = models.TextField(default="")
	dest = models.CharField(max_length=200,default="name")

class Dnsmasq(models.Model):


	def __str__(self):
		return self.name

	name = models.CharField(max_length=200,default="")
	params = models.TextField(default="")
	dest = models.CharField(max_length=200,default="")


class IpTables(models.Model):


	def __str__(self):
		return  self.name

	name = models.CharField(max_length=200)
	params = models.TextField()
	dest = models.CharField(max_length=200,default="")

class Interfaces(models.Model):


	def __str__(self):
		return  self.name

	name = models.CharField(max_length=200)
	params = models.TextField()
	dest = models.CharField(max_length=200,default="")

class Nodogsplash(models.Model):


	def __str__(self):
		return  self.name

	name = models.CharField(max_length=200)
	params = models.TextField()
	dest = models.CharField(max_length=200,default="")

class Hosts(models.Model):


	def __str__(self):
		return  self.name

	name = models.CharField(max_length=200)
	params = models.TextField()
	dest = models.CharField(max_length=200,default="")

class Ipset(models.Model):


	def __str__(self):
		return  self.name

	name = models.CharField(max_length=200)
	params = models.TextField()
	dest = models.CharField(max_length=200,default="")