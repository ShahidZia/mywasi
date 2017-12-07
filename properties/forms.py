# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from properties.models import Property, Image, Document

class PropertyLocationForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('location', 'number', 'prop_type', 'prop',)


class PropertyDescriptionForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('sqm', 'util_sqm', 'prop_status', 'num_bedrooms', 'num_bathrooms',
            'num_rooms', 'swimmingpool', 'storageroom', 'garden', 'balcony', 'wardrobe',
            'hydromassage', 'lift', 'penthouse', 'garage', 'ac', 'concierge', 'cleaner',
            'energetic_certificate', 'orientation', 'description',)


class PropertyPriceForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('price',)


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)


class PropertyDocumentForm(forms.ModelForm):
    class Meta:
       model = Document
       fields = ('document',)
