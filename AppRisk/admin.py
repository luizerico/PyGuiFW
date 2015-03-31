from django.contrib import admin

from AppRisk.models.host import Host, FormHost
from AppRisk.models.network import Network, FormNetwork
from AppRisk.models.url import URL, FormURL
from AppRisk.models.interface import Interface
from AppRisk.models.port import Port
from AppRisk.models.protocol import Protocol
from AppRisk.models.filter import Filter, FormFilter
from AppRisk.models.chain import Chain
from AppRisk.models.nat import Nat, FormNat
from AppRisk.models.hostset import Hostset, FormHostset
from AppRisk.models.netset import Netset, FormNetset


from django.contrib.auth.models import Permission
admin.site.register(Permission)

# Register your models here.

@admin.register(Hostset)
class SethostAdmin(admin.ModelAdmin):
    filter_horizontal = ('address',)
    form = FormHostset

    class Media:
        css = { 'all':['css/other.css',], }

@admin.register(Netset)
class SetnetAdmin(admin.ModelAdmin):
    filter_horizontal = ('address',)
    form = FormNetset

    class Media:
        css = { 'all':['css/other.css',], }

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

@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):
    pass

@admin.register(Nat)
class NatAdmin(admin.ModelAdmin):
   #inlines = ['log', 'log_level', 'log_preffix',]
    list_display = ('order','name','action','log')
    list_filter = ('order','action',)
    list_display_links = ()

    fieldsets = [
        (None, {'fields':('order','name','action','source','srcport','destiny',
                          'dstport','protocol','in_interface','out_interface',
                          'conn_state','adv_options','to_destiny','to_port', 'description')}),
        ('Log',{'classes': ('collapse','wide'),
               'fields':('log','log_level','log_preffix')})
           ]

    filter_horizontal = ('srcport', 'dstport')

    form = FormNat

    class Media:
        css = { 'all':['css/other.css',], }


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    #inlines = ['log', 'log_level', 'log_preffix',]
    list_display = ('order','name','chain','action','log')
    list_filter = ('order','action', 'chain',)
    list_display_links = ()

    fieldsets = [
        (None, {'fields':('order','name','chain','source','srcset','srcport','destiny',
                          'dstset','dstport','protocol','in_interface','out_interface',
                          'conn_state','adv_options','action','description')}),
        ('Log',{'classes': ('collapse','wide'),
               'fields':('log','log_level','log_preffix')})
           ]

    filter_horizontal = ('source', 'srcport', 'destiny', 'dstport')

    form = FormFilter

    class Media:
        css = { 'all':['css/other.css',], }