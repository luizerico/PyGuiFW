from django.contrib import admin

from models import Risk, RiskType, Asset
# Register your models here.

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    filter_horizontal = ('risk',)


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    pass

@admin.register(RiskType)
class RiskTypeAdmin(admin.ModelAdmin):
    pass


