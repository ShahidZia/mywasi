# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.validators import FileExtensionValidator

from properties.choices import *

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=254, blank=False, null=True)
    number = models.IntegerField(blank=False)
    prop_type = models.CharField(max_length=10, choices=PROP_TYPE, default='flat')
    prop = models.CharField(max_length=10, choices=PROP_TYPE, default='flat')
    price = models.FloatField()
    sqm = models.IntegerField()
    util_sqm = models.IntegerField()
    prop_status = models.CharField(max_length=10, choices=PROP_STATUS, default='good')
    num_bedrooms = models.CharField(max_length=2, choices=NUMBERS, default='1')
    num_bathrooms = models.CharField(max_length=2, choices=NUMBERS, default='1')
    num_rooms = models.CharField(max_length=2, choices=NUMBERS, default='1')
    swimmingpool = models.BooleanField(default=False)
    storageroom = models.BooleanField(default=False)
    garden = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    wardrobe = models.BooleanField(default=False)
    hydromassage = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    penthouse = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    concierge = models.BooleanField(default=False)
    cleaner = models.BooleanField(default=False)
    energetic_certificate = models.CharField(max_length=1, choices=ENERGETIC_CERTIFICATE, default='d')
    orientation = models.CharField(max_length=5, choices=ORIENTATION, default='north')
    description = models.TextField()
    #image = models.ImageField(upload_to=user_directory_path, blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    #plane = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    #energetic_certificate_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    #certificate_of_occupancy = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{}, {}'.format(self.location, self.number)

    class Meta:
        verbose_name_plural = 'Properties'


def user_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/images/<filename>
    return 'user_{0}/images/{1}'.format(instance.prop.user.id, filename)


class Image(models.Model):
   prop = models.ForeignKey(Property)
   image = models.ImageField(upload_to=user_image_directory_path, blank=True, null=True)
   uploaded_at = models.DateTimeField(auto_now_add=True)

   def __unicode__(self):
       return '{}, {}'.format(str(self.prop.location), self.image.name)


def user_document_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/images/<filename>
    return 'user_{0}/docs/{1}'.format(instance.prop.user.id, filename)


class Document(models.Model):
   prop = models.ForeignKey(Property)
   name = models.CharField(max_length=256)
   document = models.FileField(upload_to=user_document_directory_path, blank=True, null=True)
   uploaded_at = models.DateTimeField(auto_now_add=True)

   def __unicode__(self):
       return '{}, {}'.format(str(self.prop.location), self.document.name)
