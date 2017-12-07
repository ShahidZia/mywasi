# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.utils import timezone

from core.models import Valuation
from properties.models import Property, Image, Document
from properties.forms import PropertyLocationForm, PropertyDescriptionForm, PropertyPriceForm, PropertyImageForm, PropertyDocumentForm

def properties(request):
    properties = Property.objects.filter(user=request.user.id).order_by('updated')
    if len(properties) < 3:
        no_properties = range(3-len(properties))
    else:
        no_properties = {}
    return render(request, 'properties/properties.html', {'properties': properties, 'no_properties': no_properties})


def property_detail(request, pk):
    property = Property.objects.get(pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})

# ADD PROPERTY

def add_property_location(request):
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        form = PropertyLocationForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = user
            property.price = 0
            property.sqm = 0
            property.util_sqm = 0
            property.save()
        return redirect('add_property_description')

    else:
        form = PropertyLocationForm()
    return render(request, 'properties/add_edit_location.html', {'form': form})


def add_property_description(request):
    property = Property.objects.filter(user=request.user).latest('updated')
    if request.method == 'POST':
        form = PropertyDescriptionForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
        return redirect('add_property_price')

    else:
        form = PropertyDescriptionForm(instance=property)
    return render(request, 'properties/add_edit_description.html', {'form': form})


def add_property_price(request):
    property = Property.objects.filter(user=request.user).latest('updated')
    if request.method == 'POST':
        form = PropertyPriceForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
        return redirect('properties')

    else:
        form = PropertyPriceForm(instance=property)
    return render(request, 'properties/add_edit_price.html', {'form': form})

# EDIT PROPERTY

def edit_property_location(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyLocationForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
        return redirect('edit_property_description', pk)

    else:
        form = PropertyLocationForm(instance=property)
    return render(request, 'properties/add_edit_location.html', {'form': form})


def edit_property_description(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyDescriptionForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
        return redirect('edit_property_price', pk)

    else:
        form = PropertyDescriptionForm(instance=property)
    return render(request, 'properties/add_edit_description.html', {'form': form})


def edit_property_price(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyPriceForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
        return redirect('edit_property_images', pk)

    else:
        form = PropertyPriceForm(instance=property)
    return render(request, 'properties/add_edit_price.html', {'form': form})


class ImageUploadView(View):
    def get(self, request, pk):
        photo_list = Image.objects.all().filter(prop=pk)
        return render(self.request, 'properties/add_edit_images.html', {'photo_list': photo_list})

    def post(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        form = PropertyImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            for f in self.request.FILES.getlist('image'):
                i = Image(prop=property, image=f)
                i.save()

        return redirect('edit_property_documents', pk=pk)


class DocumentUploadView(View):
    def get(self, request, pk):
        document_list = Document.objects.all().filter(prop=pk)
        return render(self.request, 'properties/add_edit_documents.html', {'document_list': document_list})

    def post(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        form = PropertyDocumentForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            for f in self.request.FILES.keys():
                for d in self.request.FILES.getlist(f):
                    doc = Document(prop=property, name=f, document=d)
                    doc.save()

        return redirect('properties')
