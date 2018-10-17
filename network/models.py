from django.db import models
import netifaces
from rest_framework import serializers

class Networks(models.Model):


	def __str__(self):
		return self.name




	name = models.CharField(max_length=200,default="name")
	




	




class AfLinks(models.Model):

	def __str__(self):
		return self.name



	types = (
		('AF_LINK','AF_LINK'),
		('AF_INET','AF_INET'),
		('AF_INET6','AF_INET6')
	)

	name = models.CharField(max_length=200,default="")
	af_link_addr = models.CharField(max_length=200,default="")
	af_link_broadcast= models.CharField(max_length=200,default="")
	af_link_netmask = models.CharField(max_length=200,default="")
	af_link_peer = models.CharField(max_length=200,default="")
	networks_id = models.ForeignKey(Networks, on_delete=models.CASCADE)
	type = models.CharField(
		default="",
	    max_length=200,
	    choices=types,
	)

class AfLinksSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=200)
	af_link_addr = serializers.CharField(max_length=200)
	af_link_broadcast= serializers.CharField(max_length=200)
	af_link_netmask = serializers.CharField(max_length=200)
	af_link_peer = serializers.CharField(max_length=200)
	type = serializers.CharField(max_length=200)
