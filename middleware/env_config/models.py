from django.db import models
from pathlib import Path
from rest_framework import serializers


modes = (
	('commun','commun'),
	('wlan','wlan'),
	('eth','eth')
)

class Env(models.Model):


	def __str__(self):
		return self.name


	ts = (
		(30,'30 minute'),
		(60,'1 heure')
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

	git_repo = models.CharField(max_length=200,default="")
	git_repo_update = models.CharField(max_length=200,default="")
	repo_dir_update = models.CharField(max_length=200,default="")
	repo_dir = models.CharField(max_length=200,default="")
	middleware_dir = models.CharField(max_length=200,default="middleware")
	databases_backup_dir = models.CharField(max_length=200,default="databases_backups")
	config_dir = models.CharField(max_length=200,default="opt/config/")

	ftp_host = models.CharField(max_length=200,default="127.0.0.1")
	ftp_user = models.CharField(max_length=200,default="user")
	ftp_password = models.CharField(max_length=200,default="password")

	ssid_prefix = models.CharField(max_length=200,default="_FREE_WIFI")


	api_mode = models.CharField(
	    max_length=200,
	    choices=modes,
	)
	client_session_timeout = models.IntegerField(
	    choices=ts,
	    default=30
	)


class EnvSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=200)
	api_host = serializers.CharField(max_length=200)
	api_key = serializers.CharField(max_length=200)
	api_secret = serializers.CharField(max_length=200)
	api_port = serializers.CharField(max_length=200)
	root_dir = serializers.CharField(max_length=200)
	version = serializers.CharField(max_length=200)
	patch = serializers.CharField(max_length=200)
	app_dir = serializers.CharField(max_length=200)
	git_repo = serializers.CharField(max_length=200)

	ftp_host = serializers.CharField(max_length=200)
	ftp_user = serializers.CharField(max_length=200)
	ftp_password = serializers.CharField(max_length=200)

	ssid_prefix = serializers.CharField(max_length=200)
	client_session_timeout = serializers.IntegerField()
	api_mode = serializers.CharField(max_length=200)

class SettingTypes(models.Model):

	def __str__(self):
		return self.name

	name = models.CharField(max_length=200,default="")

class SettingApp(models.Model):


	def __str__(self):
		return self.name


	shell_types = (
		('sh','Sh'),
		('cmd','cmd')
	)

	name = models.CharField(max_length=200,default="")
	directory = models.CharField(max_length=200,default="",blank=True)
	sub_directory = models.CharField(max_length=200,default="",blank=True)
	params = models.TextField(default="")
	api_mode = models.CharField(
	    max_length=200,
	    choices=modes,
	)
	setting_type = models.ForeignKey(SettingTypes, on_delete=models.CASCADE)

	origine = models.CharField(max_length=200,default="")
	dest = models.CharField(max_length=200,default="")
	cmd = models.CharField(max_length=200,default="",blank=True)
	command_type = models.CharField(
	    max_length=200,
	    choices=shell_types,
	    default="cmd"
	)
	cmd_next = models.CharField(max_length=200,default="",blank=True)
	command_type_next = models.CharField(
	    max_length=200,
	    choices=shell_types,
	    default="cmd"
	)
	sequence = models.IntegerField(default=0)
	active = models.BooleanField(default=True)

class SettingAppSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=200)
	directory = serializers.CharField(max_length=200)
	sub_directory = serializers.CharField(max_length=200)
	params = serializers.CharField(max_length=200)
	api_mode = serializers.CharField(max_length=200)
	setting_type = serializers.CharField(max_length=200)
	origine = serializers.CharField(max_length=200)
	dest = serializers.CharField(max_length=200)
	cmd =  serializers.CharField(max_length=200)
	command_type = serializers.CharField(max_length=200)
	cmd_next = serializers.CharField(max_length=200)
	command_type_next = serializers.CharField(max_length=200)
	sequence = serializers.IntegerField()
	active = serializers.BooleanField()


class InstalledSoftwares(models.Model):

	def __str__(self):
		return self.name

	name = models.CharField(max_length=200,default="")
	command = models.CharField(max_length=200,default="")
