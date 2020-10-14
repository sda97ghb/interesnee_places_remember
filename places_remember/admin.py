from django.contrib import admin
from places_remember import models


class PlaceInline(admin.StackedInline):
    model = models.Place
    extra = 1


class MemoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "text"]}),
        ("User", {"fields": ["user"]})
    ]
    inlines = [PlaceInline]


admin.site.register(models.Place)
admin.site.register(models.Memory, MemoryAdmin)
