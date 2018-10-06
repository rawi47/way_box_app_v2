from django.db import models
import getpass


class User(models.Model):

	def __str__(self):
		return self.name


	name = models.CharField(max_length=200,default=getpass.getuser())
	password = models.CharField(max_length=200)
