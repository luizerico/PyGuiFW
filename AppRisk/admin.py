from django.contrib import admin
from AppRisk.models.host import Host
from AppRisk.models.network import Network
from AppRisk.models.url import URL
from AppRisk.models.interface import Interface
from AppRisk.models.port import Port
from AppRisk.models.protocol import Protocol
from AppRisk.models.rule import Rule

# Register your models here.

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    pass

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    pass

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    pass

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
     filter_horizontal = ('source', 'destiny', 'port', 'protocol', )