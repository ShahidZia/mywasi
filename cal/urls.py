# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from cal import views

urlpatterns = [
    # Calendar
    #url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^calendar/$', views.EventView.as_view(), name='calendar'),
    url(r'^calendar/view/(?P<pk>[0-9]+)/$', views.event_view, name='event_view'),
    url(r'^calendar/edit/(?P<pk>[0-9]+)/$', views.event_edit, name='event_edit'),
]
