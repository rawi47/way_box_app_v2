from django.db import models
import django


class BoxStatus(models.Model):


    dhcpd_running = models.BooleanField(verbose_name='DHCPD')
    dhcpd_message = models.CharField(max_length=65535, blank=True, null=True)

    dnsmasq_running = models.BooleanField(verbose_name='DNSMASQ')
    dnsmasq_message = models.CharField(max_length=65535, blank=True, null=True)

    hostapd_running = models.BooleanField(verbose_name='HOSTAPD')
    hostapd_message = models.CharField(max_length=65535, blank=True, null=True)

    nodogsplash_running = models.BooleanField(verbose_name='NDS')
    nodogsplash_message = models.CharField(max_length=65535, blank=True, null=True)  # noqa: E501

    internet_connection_active = models.BooleanField(verbose_name='internet')
    internet_connection_message = models.CharField(max_length=65535, blank=True, null=True)  # noqa: E501

    connected_customers = models.PositiveIntegerField(verbose_name='customers')


class Patches(models.Model):


    def __str__(self):
        return self.name

    name = models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    @property
    def scripts(self):
    	return self.script_set.all()

class Script(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    code = models.FileField(upload_to='uploads/')
    sequence = models.PositiveIntegerField(default=0)
    patches_id = models.ForeignKey(Patches, on_delete=models.CASCADE)
