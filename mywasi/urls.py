# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django_private_chat import urls as django_private_chat_urls
from core import views as core_views

urlpatterns = [
    # Admin & home
    url(r'^admin/', admin.site.urls),

    # Core
    url(r'', include('core.urls')),

    # Accounts
    url(r'', include('accounts.urls')),

    # Dashboard
    # Properties
    url(r'', include('properties.urls')),

    # Calendar
    url(r'', include('cal.urls')),

    # Core
    url(r'', include('core.urls')),

    # Offers
    url(r'', include('offers.urls')),

    # Blog
    url(r'', include('blog.urls')),

    #chat
    url(r'^', include('django_private_chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
