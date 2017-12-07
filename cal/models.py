# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from properties.models import Property

class Event(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, blank=False)
    description = models.TextField()
    day = models.DateTimeField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('event_view', args=[self.pk])
        #popover_content = str(self.day) + str(self.buyer.profile.phone)
        return u'<a href="%s">%s</a>' % (url, str(self.title))
