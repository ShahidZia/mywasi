# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from properties import views

urlpatterns = [
    # Properties
    url(r'^properties/$', views.properties, name='properties'),
    url(r'^properties/detail/(?P<pk>[0-9]+)/$', views.property_detail, name='property_detail'),
    url(r'^properties/add/location/$', views.add_property_location, name='add_property_location'),
    url(r'^properties/add/description/$', views.add_property_description, name='add_property_description'),
    url(r'^properties/add/price/$', views.add_property_price, name='add_property_price'),
    url(r'^properties/edit/location/(?P<pk>[0-9]+)/$', views.edit_property_location, name='edit_property_location'),
    url(r'^properties/edit/description/(?P<pk>[0-9]+)/$', views.edit_property_description, name='edit_property_description'),
    url(r'^properties/edit/price/(?P<pk>[0-9]+)/$', views.edit_property_price, name='edit_property_price'),
    url(r'^properties/edit/images/(?P<pk>[0-9]+)/$', views.ImageUploadView.as_view(), name='edit_property_images'),
    url(r'^properties/edit/documents/(?P<pk>[0-9]+)/$', views.DocumentUploadView.as_view(), name='edit_property_documents'),
]
