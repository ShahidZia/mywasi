# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin

from offers.models import Offer

class OfferAdmin(admin.ModelAdmin):
    readonly_fields = ('offer_date', 'last_update',)

admin.site.register(Offer, OfferAdmin)
