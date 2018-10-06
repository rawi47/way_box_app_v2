from django.db import models


class CostumeLogging(models.Model):
	date = models.DateTimeField(auto_now_add=True, blank=True)
	internet = models.CharField(max_length=200)
	ip_adress = models.CharField(max_length=200)
	nodogsplash_status = models.CharField(max_length=200)
	hostapd_status = models.CharField(max_length=200)