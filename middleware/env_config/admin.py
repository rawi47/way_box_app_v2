from django.contrib import admin

from .models import Env,SettingApp,InstalledSoftwares,SettingTypes

admin.site.register(Env)
admin.site.register(SettingApp)
admin.site.register(InstalledSoftwares)
admin.site.register(SettingTypes)
