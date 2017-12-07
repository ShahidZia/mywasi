# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from blog import views

urlpatterns = [
    # Blog
    url(r'^blog/$', views.blog_home, name='blog'),
    url(r'^blog/post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^blog/settings/$', views.blog_settings, name='blog_settings'),
    url(r'^blog/post/settings/new/$', views.post_new, name='post_new'),
    url(r'^blog/post/settings/publish/(?P<pk>[0-9]+)/$', views.post_publish, name='post_publish'),
    url(r'^blog/post/settings/unpublish/(?P<pk>[0-9]+)/$', views.post_unpublish, name='post_unpublish'),
    url(r'^blog/post/settings/edit/(?P<pk>[0-9]+)/$', views.post_edit, name='post_edit'),
    url(r'^blog/post/settings/delete/(?P<pk>[0-9]+)/$', views.post_delete, name='post_delete'),
    url(r'^blog/comment/settings/(?P<pk>[0-9]+)/$', views.comment_settings, name='comment_settings'),
    url(r'^blog/comment/settings/delete/(?P<pk>[0-9]+)/$', views.comment_delete, name='comment_delete'),
]
