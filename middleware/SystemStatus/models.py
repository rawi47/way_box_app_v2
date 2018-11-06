from django.db import models
from rest_framework import serializers

class SystemStatus(models.Model):

    def __str__(self):
        return str(self.date)


    date = models.DateTimeField(auto_now_add=True, blank=True)

    dhcpcd = models.BooleanField(default=False)
    dhcpcd_message = models.TextField(default="")

    dnsmasq = models.BooleanField(default="")
    dnsmasq_message = models.TextField(default="")

    hostapd = models.BooleanField(default=False)
    hostapd_message = models.TextField(default="")

    nodogsplash = models.BooleanField(default=False)
    nodogsplash_message = models.TextField(default="")

    internet_connection = models.BooleanField(default=False)
    internet_connection_message = models.TextField(default="")

class SystemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemStatus
        exclude = ('id','date')
