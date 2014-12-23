from django.conf.urls import patterns, include, url
from AppRisk import views
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'MRisk.views.home', name='home'),
                       url('list/$', views.RuleListView.as_view(), name='list'),
                       url('edit/$', views.RuleEditView.as_view(), name='edit'),
                       url('ruleview/$', views.rule_view, name='ruleview'),
                       url('networkview/$', views.network_view, name='networkview'),
                       )

