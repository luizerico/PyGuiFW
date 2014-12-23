from django.contrib import admin
from AppRisk.models.host import Host, FormHost
from AppRisk.models.network import Network, FormNetwork
from AppRisk.models.url import URL, FormURL
from AppRisk.models.interface import Interface
from AppRisk.models.port import Port
from AppRisk.models.protocol import Protocol
from AppRisk.models.rule import Rule

# Register your models here.

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    form = FormHost

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    form = FormNetwork

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    form = FormURL

@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    pass

@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    pass

@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    pass

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
     filter_horizontal = ('source', 'srcport', 'destiny', 'dstport')