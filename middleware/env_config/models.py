from django.db import models
from pathlib import Path
from rest_framework import serializers


modes = (
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
	api_port = models.IntegerField(default=5000)

	root_dir = models.CharField(max_length=200,default=str(Path.home()))
	app_dir = models.CharField(max_length=200,default="way_box_app_v2")

	git_repo = models.CharField(max_length=200,default="")
	branch = models.CharField(max_length=200,default="master")
	commit_hash = models.CharField(max_length=200,default="")
	portal_url = models.CharField(max_length=200,default="portal.way-connect.com")


	config_dir = models.CharField(max_length=200,default="opt/config/")
	origin_config_dir = models.CharField(max_length=200,default="opt/original files/")
	etc_dir = models.CharField(max_length=200,default="/etc")


	ssid_prefix = models.CharField(max_length=200,default="_FREE_WIFI")
	run_on_start = models.BooleanField(default=True)


	api_mode = models.CharField(
	    max_length=200,
	    choices=modes,
	)
	client_session_timeout = models.IntegerField(
	    choices=ts,
	    default=30
	)
	password = models.CharField(max_length=200,default="")


class EnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Env
        exclude = ('id',)
