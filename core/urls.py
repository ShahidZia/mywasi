# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from core import views

urlpatterns = [
    # Landingpage
    url(r'^$', views.home, name='home'),

    # Pricing
    url(r'^pricing/$', views.pricing, name='pricing'),

    # Documents
    url(r'^documents/$', views.documents, name='documents'),

    # Valuation
    url(r'^valuation/$', views.valuation, name='valuation'),
]
