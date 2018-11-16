from django.db import models
import django


class BoxStatus(models.Model):

    def __str__(self):
        return str(self.date)

    date = models.DateTimeField(auto_now_add=True, blank=True)
    date_update = models.DateTimeField(auto_now_add=True, blank=True)
    dhcpcd = models.BooleanField(default=False)
    dhcpcd_message = models.TextField(default="")
    dnsmasq = models.BooleanField(default="")
    dnsmasq_message = models.TextField(default="")
    hostapd = models.BooleanField(default=False)
    hostapd_message = models.TextField(default="")
    nodogsplash = models.BooleanField(default=False)
    connected_clients = models.IntegerField(default=0)
    nodogsplash_message = models.TextField(default="")
    internet_connection = models.BooleanField(default=False)
    internet_connection_message = models.TextField(default="")
    patch_version = models.CharField(max_length=200, default="")
    branch = models.CharField(max_length=200, default="")
    git_hash = models.CharField(max_length=200, default="")


class Patches(SafeDeleteModel):


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
