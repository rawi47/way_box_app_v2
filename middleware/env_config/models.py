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
	origin_config_dir = models.CharField(max_length=200,default="opt/original files/")

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
