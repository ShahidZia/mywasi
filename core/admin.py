# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin

from core.models import Valuation

class ValuationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location', 'number', 'prop', 'prop_type')

admin.site.register(Valuation, ValuationAdmin)
