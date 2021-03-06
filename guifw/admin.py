from django.contrib import admin

from guifw.models.host import Host, FormHost
from guifw.models.network import Network, FormNetwork
from guifw.models.url import URL, FormURL
from guifw.models.interface import Interface
from guifw.models.port import Port
from guifw.models.protocol import Protocol
from guifw.models.filter import Filter, FormFilter
from guifw.models.chain import Chain
from guifw.models.nat import Nat, FormNat
from guifw.models.hostset import Hostset, FormHostset
from guifw.models.netset import Netset, FormNetset
from guifw.models.shappclass import Shappclass
from guifw.models.shapping import Shapping
from guifw.models.setting import Setting


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


@admin.register(Shappclass)
class SahppclassAdmin(admin.ModelAdmin):
    pass

@admin.register(Shapping)
class ShappingAdmin(admin.ModelAdmin):
    pass

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass