# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin

from properties.models import Property, Image, Document

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'sqm', 'prop_status', 'price', 'updated')

admin.site.register(Property, PropertyAdmin)


class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ('uploaded_at',)

admin.site.register(Image, ImageAdmin)


class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('uploaded_at',)

admin.site.register(Document, DocumentAdmin)
