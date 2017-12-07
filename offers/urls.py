# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from offers import views

urlpatterns = [
    # Offers
    url(r'^offers/$', views.list_offers, name='list_offers'),
    url(r'^offers/make/$', views.make_offer, name='make_offer'),
    url(r'^offers/comment/$', views.comment_offer, name='comment_offer'),
    url(r'^offers/feedback/refused/(?P<pk>[0-9]+)/$', views.refuse_feedback, name='refuse_feedback'),
    url(r'^offers/feedback/canceled/(?P<pk>[0-9]+)/$', views.cancel_feedback, name='cancel_feedback'),
    # url(r'^offers/edit/(?P<pk>[0-9]+)/$', views.edit_offer, name='edit_offer'),
    url(r'^offers/accept/(?P<pk>[0-9]+)/$', views.accept_offer, name='accept_offer'),
    # url(r'^offers/refuse/(?P<pk>[0-9]+)/$', views.refuse_offer, name='refuse_offer'),
    # url(r'^offers/cancel/(?P<pk>[0-9]+)/$', views.cancel_offer, name='cancel_offer'),
]
