from django.conf.urls import patterns, include, url
from AppRisk import views
from AppRisk.views.host_view import *
from AppRisk.views.network_view import *

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'MRisk.views.home', name='home'),
                       # url('list/$', views.RuleListView.as_view(), name='list'),
                       #url('edit/$', views.RuleEditView.as_view(), name='edit'),
                       #url('ruleview/$', views.rule_view, name='ruleview'),
                       #url('networkview/$', views.network_view, name='networkview'),
                       #url('rulecomposerview/$', views.ruleComposerView, name='composerview'),

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

)

