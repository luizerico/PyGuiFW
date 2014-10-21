from django.conf.urls import patterns, include, url
from AppRisk import views
from django.contrib import admin


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'MRisk.views.home', name='home'),
                       url('list/$', views.AssetListView.as_view(), name='list'),
                       url('edit/$', views.AssetEditView.as_view(), name='edit'),
                       )

