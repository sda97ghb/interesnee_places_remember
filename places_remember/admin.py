from django.contrib import admin
from places_remember import models
from django.utils.translation import gettext_lazy as _


class PlaceInline(admin.StackedInline):
    model = models.Place
    extra = 1


class MemoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "text"]}),
        (_("User"), {"fields": ["user"]})
    ]
    inlines = [PlaceInline]


admin.site.register(models.Place)
admin.site.register(models.Memory, MemoryAdmin)
