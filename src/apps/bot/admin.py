from django.contrib import admin

from .forms import FundAdminForm
from .models import AgeLimit, City, Country, Fund, Region


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_filter = ("country",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_filter = ("region__country", "region")


@admin.register(AgeLimit)
class АgeLimitAdmin(admin.ModelAdmin):
    pass


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    form = FundAdminForm
    list_display = ("name", "age_limit")
