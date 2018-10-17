from django.contrib import admin

from .models import Env,SettingApp,InstalledSoftwares

admin.site.register(Env)
admin.site.register(SettingApp)
admin.site.register(InstalledSoftwares)
