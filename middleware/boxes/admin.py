from django.contrib import admin
from .models import Patch, Script
from safedelete.admin import highlight_deleted, SafeDeleteAdmin

class ScriptInline(admin.TabularInline):
    model = Script
    ordering = ('sequence',)


@admin.register(Patch)
class PatchAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted, 'created_at',
        *SafeDeleteAdmin.list_display
    )

    search_fields = (
        'name',
        *SafeDeleteAdmin.list_filter
    )

    inlines = (ScriptInline,)
