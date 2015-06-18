from django.conf.urls import patterns, include, url
from guifw import views
from guifw.views.host_view import *
from guifw.views.network_view import *
from guifw.views.url_view import *
from guifw.views.protocol_view import *
from guifw.views.port_view import *
from guifw.views.chain_view import *
from guifw.views.hostset_view import *
from guifw.views.netset_view import *
from guifw.views.filter_view import *
from guifw.views.nat_view import *
from guifw.views.interface_view import *
from guifw.views.auth import *
from guifw.views.trafficclass_view import *
from guifw.views.traffic_view import *

from guifw.views.general import *

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'PyGUIFW.views.home', name='home'),
                       url(r'^$', permission_required('guifw.view_rules', login_url='login')(ruleView), name='rule-view'),

                       # System URL
                       url('ruleview/$', permission_required('guifw.view_rules')(ruleView), name='rule-view'),
                       url('ruleapply/$', permission_required('guifw.edit_rules')(ruleApply), name='rule-apply'),
                       url('rulesave/$', permission_required('guifw.edit_rules')(ruleSave), name='rule-save'),

                       url('processes/$', permission_required('guifw.view_rules')(listProcesses), name='processes'),
                       url('routes/$', permission_required('guifw.view_rules')(listRoutes), name='routes'),
                       url('interfaces/$', permission_required('guifw.view_rules')(listInterfaces), name='interfaces'),
                       url('connections/$', permission_required('guifw.view_rules')(listConnections), name='connections'),
                       url('about/$', permission_required('guifw.view_rules')(listConnections), name='about'),

                       #url('login/$', permission_required('guifw.edit_rules')(login_view),
                       url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}, name='login'),
                       url(r'^logout/$', logout_view, name='logout'),
                       url(r'^denied/$', denied_view, name='denied'),

                       # Hosts URLs Configuration
                       url(r'^host/list/$', permission_required('guifw.view_rules')(HostList.as_view()), name='host-list'),
                       url(r'^host/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(HostDetail.as_view()), name='host-detail'),
                       url(r'^host/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='host-multidelete'),
                       url(r'^host/create/$', permission_required('guifw.edit_rules')(HostCreate.as_view()), name='host-create'),
                       url(r'^host/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(HostUpdate.as_view()), name='host-edit'),
                       url(r'^host/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(HostDelete.as_view()), name='host-delete'),

                       #Network URLs Configuration
                       url(r'^network/list/$', permission_required('guifw.view_rules')(NetworkList.as_view()), name='network-list'),
                       url(r'^network/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(NetworkDetail.as_view()), name='network-detail'),
                       url(r'^network/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='network-multidelete'),
                       url(r'^network/create/$', permission_required('guifw.edit_rules')(NetworkCreate.as_view()), name='network-create'),
                       url(r'^network/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(NetworkUpdate.as_view()), name='network-edit'),
                       url(r'^network/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(NetworkDelete.as_view()), name='network-delete'),

                       #Url URLs Configuration
                       url(r'^url/list/$', permission_required('guifw.view_rules')(URLList.as_view()), name='url-list'),
                       url(r'^url/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(URLDetail.as_view()), name='url-detail'),
                       url(r'^url/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='url-multidelete'),
                       url(r'^url/create/$', permission_required('guifw.edit_rules')(URLCreate.as_view()), name='url-create'),
                       url(r'^url/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(URLUpdate.as_view()), name='url-edit'),
                       url(r'^url/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(URLDelete.as_view()), name='url-delete'),

                       #Protocols URLs Configuration
                       url(r'^protocol/list/$', permission_required('guifw.view_rules')(ProtocolList.as_view()), name='protocol-list'),
                       url(r'^protocol/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(ProtocolDetail.as_view()), name='protocol-detail'),
                       url(r'^protocol/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='protocol-multidelete'),
                       url(r'^protocol/create/$', permission_required('guifw.edit_rules')(ProtocolCreate.as_view()), name='protocol-create'),
                       url(r'^protocol/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(ProtocolUpdate.as_view()), name='protocol-edit'),
                       url(r'^protocol/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(ProtocolDelete.as_view()), name='protocol-delete'),

                       #Ports URLs Configuration
                       url(r'^port/list/$', permission_required('guifw.view_rules')(PortList.as_view()), name='port-list'),
                       url(r'^port/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(PortDetail.as_view()), name='port-detail'),
                       url(r'^port/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='port-multidelete'),
                       url(r'^port/create/$', permission_required('guifw.edit_rules')(PortCreate.as_view()), name='port-create'),
                       url(r'^port/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(PortUpdate.as_view()), name='port-edit'),
                       url(r'^port/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(PortDelete.as_view()), name='port-delete'),

                       #Chains URLs Configuration
                       url(r'^chain/list/$', permission_required('guifw.view_rules')(ChainList.as_view()), name='chain-list'),
                       url(r'^chain/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(ChainDetail.as_view()), name='chain-detail'),
                       url(r'^chain/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='chain-multidelete'),
                       url(r'^chain/create/$', permission_required('guifw.edit_rules')(ChainCreate.as_view()), name='chain-create'),
                       url(r'^chain/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(ChainUpdate.as_view()), name='chain-edit'),
                       url(r'^chain/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(ChainDelete.as_view()), name='chain-delete'),

                       #Hostset URLs Configuration
                       url(r'^hostset/list/$', permission_required('guifw.view_rules')(HostsetList.as_view()), name='hostset-list'),
                       url(r'^hostset/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(HostsetDetail.as_view()), name='hostset-detail'),
                       url(r'^hostset/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='hostset-multidelete'),
                       url(r'^hostset/create/$', permission_required('guifw.edit_rules')(HostsetCreate.as_view()), name='hostset-create'),
                       url(r'^hostset/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(HostsetUpdate.as_view()), name='hostset-edit'),
                       url(r'^hostset/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(HostsetDelete.as_view()), name='hostset-delete'),

                       #Netset URLs Configuration
                       url(r'^netset/list/$', permission_required('guifw.view_rules')(NetsetList.as_view()), name='netset-list'),
                       url(r'^netset/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(NetsetDetail.as_view()), name='netset-detail'),
                       url(r'^netset/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='netset-multidelete'),
                       url(r'^netset/create/$', permission_required('guifw.edit_rules')(NetsetCreate.as_view()), name='netset-create'),
                       url(r'^netset/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(NetsetUpdate.as_view()), name='netset-edit'),
                       url(r'^netset/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(NetsetDelete.as_view()), name='netset-delete'),


                       #Filters URLs Configuration
                       url(r'^filter/list/$', permission_required('guifw.view_rules')(FilterList.as_view()), name='filter-list'),
                       url(r'^filter/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(FilterDetail.as_view()), name='filter-detail'),
                       url(r'^filter/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='filter-multidelete'),
                       url(r'^filter/create/$', permission_required('guifw.edit_rules')(FilterCreate.as_view()), name='filter-create'),
                       url(r'^filter/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(FilterUpdate.as_view()), name='filter-edit'),
                       url(r'^filter/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(FilterDelete.as_view()), name='filter-delete'),
                       url(r'^filter/reorder/(?P<order_id>\d+)/$', permission_required('guifw.edit_rules')(FilterReorder), name='filter-reorder'),
                       url(r'^filter/reorderup/(?P<order_id>\d+)/$', permission_required('guifw.edit_rules')(FilterReorderUp), name='filter-reorderup'),
                       url(r'^filter/reorderdown/(?P<order_id>\d+)/$', permission_required('guifw.edit_rules')(FilterReorderDown), name='filter-reorderdown'),

                       #NAT URLs Configuration
                       url(r'^nat/list/$', permission_required('guifw.view_rules')(NatList.as_view()), name='nat-list'),
                       url(r'^nat/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(NatDetail.as_view()), name='nat-detail'),
                       url(r'^nat/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='nat-multidelete'),
                       url(r'^nat/create/$', permission_required('guifw.edit_rules', login_url='denied')(NatCreate.as_view()), name='nat-create'),
                       url(r'^nat/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules', login_url='denied')(NatUpdate.as_view()), name='nat-edit'),
                       url(r'^nat/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules', login_url='denied')(NatDelete.as_view()), name='nat-delete'),

                       #Interface URLs Configuration
                       url(r'^interface/list/$', permission_required('guifw.view_rules')(InterfaceList.as_view()), name='interface-list'),
                       url(r'^interface/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(InterfaceDetail.as_view()), name='interface-detail'),
                       url(r'^interface/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='interface-multidelete'),
                       url(r'^interface/create/$', permission_required('guifw.edit_rules')(InterfaceCreate.as_view()), name='interface-create'),
                       url(r'^interface/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(InterfaceUpdate.as_view()), name='interface-edit'),
                       url(r'^interface/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(InterfaceDelete.as_view()), name='interface-delete'),

                       #Trafficclass URLs Configuration
                       url(r'^trafficclass/list/$', permission_required('guifw.view_rules')(TrafficclassList.as_view()), name='trafficclass-list'),
                       url(r'^trafficclass/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(TrafficclassDetail.as_view()), name='trafficclass-detail'),
                       url(r'^trafficclass/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='trafficclass-multidelete'),
                       url(r'^trafficclass/create/$', permission_required('guifw.edit_rules')(TrafficclassCreate.as_view()), name='trafficclass-create'),
                       url(r'^trafficclass/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(TrafficclassUpdate.as_view()), name='trafficclass-edit'),
                       url(r'^trafficclass/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(TrafficclassDelete.as_view()), name='trafficclass-delete'),

                       #Traffic URLs Configuration
                       url(r'^traffic/list/$', permission_required('guifw.view_rules')(TrafficList.as_view()), name='traffic-list'),
                       url(r'^traffic/detail/(?P<pk>\d+)/$', permission_required('guifw.view_rules')(TrafficDetail.as_view()), name='traffic-detail'),
                       url(r'^traffic/multidelete/$', permission_required('guifw.edit_rules')(multipleDelete), name='traffic-multidelete'),
                       url(r'^traffic/create/$', permission_required('guifw.edit_rules')(TrafficCreate.as_view()), name='traffic-create'),
                       url(r'^traffic/edit/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(TrafficUpdate.as_view()), name='traffic-edit'),
                       url(r'^traffic/delete/(?P<pk>\d+)/$', permission_required('guifw.edit_rules')(TrafficDelete.as_view()), name='traffic-delete'),

)

