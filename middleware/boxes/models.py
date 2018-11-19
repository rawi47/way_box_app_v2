from safedelete.models import SafeDeleteModel, SOFT_DELETE
from django.db import models
import django


class Patch(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

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
    patch = models.ForeignKey(Patch, on_delete=models.CASCADE)
