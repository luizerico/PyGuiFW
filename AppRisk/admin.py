from django.contrib import admin
from AppRisk.models.host import Host, FormHost
from AppRisk.models.network import Network, FormNetwork
from AppRisk.models.url import URL, FormURL
from AppRisk.models.interface import Interface
from AppRisk.models.port import Port
from AppRisk.models.protocol import Protocol
from AppRisk.models.filter import Filter, FilterForm
from AppRisk.models.action import Action
from AppRisk.models.loglevel import LogLevel
from AppRisk.models.chain import Chain
from AppRisk.models.nat import Nat


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

#@admin.register(Action)
#class ActionAdmin(admin.ModelAdmin):
#    pass

@admin.register(LogLevel)
class LogLevelAdmin(admin.ModelAdmin):
    pass

@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):
    pass

@admin.register(Nat)
class NatAdmin(admin.ModelAdmin):
    pass

@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    #inlines = ['log', 'log_level', 'log_preffix',]
    list_display = ('order','name','chain','action','log')
    list_filter = ('order','action', 'chain',)
    list_display_links = ()

    fieldsets = [
        (None, {'fields':('order','name','chain','source','srcport','destiny',
                          'dstport','protocol','in_interface','out_interface',
                          'conn_state','adv_options','action','description')}),
        ('Log',{'classes': ('collapse','wide'),
               'fields':('log','log_level','log_preffix')})
           ]

    filter_horizontal = ('source', 'srcport', 'destiny', 'dstport')

    form = FilterForm

    class Media:
        css = { 'all':['css/other.css',], }