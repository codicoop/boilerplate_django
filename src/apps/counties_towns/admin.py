from django.contrib import admin

from apps.counties_towns.models import County, Town


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    pass


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    pass
