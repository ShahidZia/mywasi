# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

from accounts.models import Profile


class Valuation(models.Model):
    user = models.ForeignKey(User, null=True)
    location = models.CharField(max_length=254, blank=True)
    number = models.IntegerField(blank=True)
    prop = models.CharField(max_length=254, blank=True)
    prop_type = models.CharField(max_length=254, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '{}, {}'.format(self.location, self.number)
