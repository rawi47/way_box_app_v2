from django.contrib import admin
from safedelete.admin import highlight_deleted, SafeDeleteAdmin
from .models import BoxStatus, Patches, Script, UpdateInformation

admin.site.register(BoxStatus)
admin.site.register(Patches)
