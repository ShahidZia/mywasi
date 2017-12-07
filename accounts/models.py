# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.choices import *

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/profile/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=False, null=True)
    dni = models.CharField(max_length=9, blank=True, null=True)
    company_name = models.CharField(max_length=254, blank=True)
    nif = models.CharField(max_length=10, blank=True)
    billing_address = models.CharField(max_length=254, blank=True)
    business_email = models.EmailField(blank=True)
    status = models.CharField(max_length=10, choices=USER_STATUS, default='seller')


    def __unicode__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()
