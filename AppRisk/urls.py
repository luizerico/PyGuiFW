from django.conf.urls import patterns, include, url
from AppRisk import views
from AppRisk.views.host_view import *
from AppRisk.views.network_view import *
from AppRisk.views.url_view import *
from AppRisk.views.protocol_view import *
from AppRisk.views.port_view import *
from AppRisk.views.chain_view import *
from AppRisk.views.hostset_view import *
from AppRisk.views.netset_view import *
from AppRisk.views.filter_view import *
from AppRisk.views.nat_view import *
from AppRisk.views.interface_view import *

from AppRisk.views.general import *

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'MRisk.views.home', name='home'),
                       # url('list/$', views.RuleListView.as_view(), name='list'),
                       #url('edit/$', views.RuleEditView.as_view(), name='edit'),
                       #url('ruleview/$', views.rule_view, name='ruleview'),
                       #url('networkview/$', views.network_view, name='networkview'),
                       url('rulecomposerview/$', ruleComposerView, name='composerview'),
                       url('infall/$', listInterfaces, name='infall'),


                       # System URL
                       url('routes/$', listRoutes, name='routes'),
                       url('interfaces/$', listInterfaces, name='interfaces'),
                       url('connections/$', listConnections, name='connections'),

                       url(r'^dynamic-media/jsi18n/$', 'django.views.i18n.javascript_catalog'),
                       # Definitions of Risk URL
                       url(r'^$', HostList.as_view(), name='host-list'),

                       # Hosts URLs Configuration
                       url(r'^host/multidelete/$', multipleDelete, name='host-multidelete'),
                       url(r'^host/list/$', HostList.as_view(), name='host-list'),
                       url(r'^host/create/$', HostCreate.as_view(), name='host-create'),
                       url(r'^host/detail/(?P<pk>\d+)/$', HostDetail.as_view(), name='host-detail'),
                       url(r'^host/edit/(?P<pk>\d+)/$', HostUpdate.as_view(), name='host-edit'),
                       url(r'^host/delete/(?P<pk>\d+)/$', HostDelete.as_view(), name='host-delete'),

                       #Network URLs Configuration
                       url(r'^network/multidelete/$', multipleDelete, name='network-multidelete'),
                       url(r'^network/list/$', NetworkList.as_view(), name='network-list'),
                       url(r'^network/create/$', NetworkCreate.as_view(), name='network-create'),
                       url(r'^network/detail/(?P<pk>\d+)/$', NetworkDetail.as_view(), name='network-detail'),
                       url(r'^network/edit/(?P<pk>\d+)/$', NetworkUpdate.as_view(), name='network-edit'),
                       url(r'^network/delete/(?P<pk>\d+)/$', NetworkDelete.as_view(), name='network-delete'),

                       #Url URLs Configuration
                       url(r'^url/multidelete/$', multipleDelete, name='url-multidelete'),
                       url(r'^url/list/$', URLList.as_view(), name='url-list'),
                       url(r'^url/create/$', URLCreate.as_view(), name='url-create'),
                       url(r'^url/detail/(?P<pk>\d+)/$', URLDetail.as_view(), name='url-detail'),
                       url(r'^url/edit/(?P<pk>\d+)/$', URLUpdate.as_view(), name='url-edit'),
                       url(r'^url/delete/(?P<pk>\d+)/$', URLDelete.as_view(), name='url-delete'),

                       #Protocols URLs Configuration
                       url(r'^protocol/multidelete/$', multipleDelete, name='protocol-multidelete'),
                       url(r'^protocol/list/$', ProtocolList.as_view(), name='protocol-list'),
                       url(r'^protocol/create/$', ProtocolCreate.as_view(), name='protocol-create'),
                       url(r'^protocol/detail/(?P<pk>\d+)/$', ProtocolDetail.as_view(), name='protocol-detail'),
                       url(r'^protocol/edit/(?P<pk>\d+)/$', ProtocolUpdate.as_view(), name='protocol-edit'),
                       url(r'^protocol/delete/(?P<pk>\d+)/$', ProtocolDelete.as_view(), name='protocol-delete'),

                       #Ports URLs Configuration
                       url(r'^port/multidelete/$', multipleDelete, name='port-multidelete'),
                       url(r'^port/list/$', PortList.as_view(), name='port-list'),
                       url(r'^port/create/$', PortCreate.as_view(), name='port-create'),
                       url(r'^port/detail/(?P<pk>\d+)/$', PortDetail.as_view(), name='port-detail'),
                       url(r'^port/edit/(?P<pk>\d+)/$', PortUpdate.as_view(), name='port-edit'),
                       url(r'^port/delete/(?P<pk>\d+)/$', PortDelete.as_view(), name='port-delete'),

                       #Chains URLs Configuration
                       url(r'^chain/multidelete/$', multipleDelete, name='chain-multidelete'),
                       url(r'^chain/list/$', ChainList.as_view(), name='chain-list'),
                       url(r'^chain/create/$', ChainCreate.as_view(), name='chain-create'),
                       url(r'^chain/detail/(?P<pk>\d+)/$', ChainDetail.as_view(), name='chain-detail'),
                       url(r'^chain/edit/(?P<pk>\d+)/$', ChainUpdate.as_view(), name='chain-edit'),
                       url(r'^chain/delete/(?P<pk>\d+)/$', ChainDelete.as_view(), name='chain-delete'),

                       #Hostset URLs Configuration
                       url(r'^hostset/multidelete/$', multipleDelete, name='hostset-multidelete'),
                       url(r'^hostset/list/$', HostsetList.as_view(), name='hostset-list'),
                       url(r'^hostset/create/$', HostsetCreate.as_view(), name='hostset-create'),
                       url(r'^hostset/detail/(?P<pk>\d+)/$', HostsetDetail.as_view(), name='hostset-detail'),
                       url(r'^hostset/edit/(?P<pk>\d+)/$', HostsetUpdate.as_view(), name='hostset-edit'),
                       url(r'^hostset/delete/(?P<pk>\d+)/$', HostsetDelete.as_view(), name='hostset-delete'),

                       #Netset URLs Configuration
                       url(r'^netset/multidelete/$', multipleDelete, name='netset-multidelete'),
                       url(r'^netset/list/$', NetsetList.as_view(), name='netset-list'),
                       url(r'^netset/create/$', NetsetCreate.as_view(), name='netset-create'),
                       url(r'^netset/detail/(?P<pk>\d+)/$', NetsetDetail.as_view(), name='netset-detail'),
                       url(r'^netset/edit/(?P<pk>\d+)/$', NetsetUpdate.as_view(), name='netset-edit'),
                       url(r'^netset/delete/(?P<pk>\d+)/$', NetsetDelete.as_view(), name='netset-delete'),


                       #Filters URLs Configuration
                       url(r'^filter/multidelete/$', multipleDelete, name='filter-multidelete'),
                       url(r'^filter/list/$', FilterList.as_view(), name='filter-list'),
                       url(r'^filter/create/$', FilterCreate.as_view(), name='filter-create'),
                       url(r'^filter/detail/(?P<pk>\d+)/$', FilterDetail.as_view(), name='filter-detail'),
                       url(r'^filter/edit/(?P<pk>\d+)/$', FilterUpdate.as_view(), name='filter-edit'),
                       url(r'^filter/delete/(?P<pk>\d+)/$', FilterDelete.as_view(), name='filter-delete'),

                       #NAT URLs Configuration
                       url(r'^nat/multidelete/$', multipleDelete, name='nat-multidelete'),
                       url(r'^nat/list/$', NatList.as_view(), name='nat-list'),
                       url(r'^nat/create/$', NatCreate.as_view(), name='nat-create'),
                       url(r'^nat/detail/(?P<pk>\d+)/$', NatDetail.as_view(), name='nat-detail'),
                       url(r'^nat/edit/(?P<pk>\d+)/$', NatUpdate.as_view(), name='nat-edit'),
                       url(r'^nat/delete/(?P<pk>\d+)/$', NatDelete.as_view(), name='nat-delete'),

                       #Interface URLs Configuration
                       url(r'^interface/multidelete/$', multipleDelete, name='interface-multidelete'),
                       url(r'^interface/list/$', InterfaceList.as_view(), name='interface-list'),
                       url(r'^interface/create/$', InterfaceCreate.as_view(), name='interface-create'),
                       url(r'^interface/detail/(?P<pk>\d+)/$', InterfaceDetail.as_view(), name='interface-detail'),
                       url(r'^interface/edit/(?P<pk>\d+)/$', InterfaceUpdate.as_view(), name='interface-edit'),
                       url(r'^interface/delete/(?P<pk>\d+)/$', InterfaceDelete.as_view(), name='interface-delete'),

)

