from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin
from .models import Env
import utils.run as rn

@admin.register(Env)
class EnvAdmin(admin.ModelAdmin):
    readonly_fields = ["name"]

    search_fields = (
        'name',
        *SafeDeleteAdmin.list_filter
    )

    def save_model(self, request, obj, form, change):
        if change:
            rn._config_main_prog()
        super().save_model(request, obj, form, change)
