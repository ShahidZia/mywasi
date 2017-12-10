# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    # Accounts
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^accounts/account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),

    # Change password
    url(r'^accounts/password/change/$', views.change_password, name='password_change'),

    # Password reset
    url(r'^accounts/password/reset/$', auth_views.password_reset, {'template_name': 'accounts/registration/password_reset_form.html'}, name='password_reset'),
    url(r'^accounts/password/reset/done/$', auth_views.password_reset_done, {'template_name': 'accounts/registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'accounts/registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$', auth_views.password_reset_complete, {'template_name': 'accounts/registration/password_reset_complete.html'}, name='password_reset_complete'),

    # Dashboard
    url(r'^settings/$', views.edit_profile, name='settings'),
    url(r'^change_status/(?P<status>[-\w]+)/$', views.change_user_status, name='change_status'),

    url(r"^lookup_users/?$", views.search_for_users, name='users-lookup')

]
