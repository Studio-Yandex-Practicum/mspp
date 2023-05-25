from django.contrib import admin
from django.contrib.auth.models import Group
from mptt.admin import MPTTModelAdmin

from .forms import FundAdminForm
from .models import AgeLimit, CoverageArea, Fund

admin.site.unregister(Group)


@admin.register(CoverageArea)
class CoverageAreaAdmin(MPTTModelAdmin):
    pass


@admin.register(AgeLimit)
class AgeLimitAdmin(admin.ModelAdmin):
    pass


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    form = FundAdminForm
    list_display = ("name", "age_limit")
