from django.contrib import admin
from safedelete.admin import highlight_deleted, SafeDeleteAdmin
from .models import BoxStatus, Patches, Script, UpdateInformation

admin.site.register(BoxStatus)


class ScriptInline(admin.TabularInline):
    model = Script
    ordering = ('sequence',)


@admin.register(Patches)
class PatchesAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted, 'created_at',
        *SafeDeleteAdmin.list_display
    )

    search_fields = (
        'name',
        *SafeDeleteAdmin.list_filter
    )

    inlines = (ScriptInline,)
