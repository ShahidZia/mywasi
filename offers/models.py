# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from properties.models import Property
from offers.choices import *

class Offer(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_type = models.CharField(max_length=10, choices=PAYMENT, default="transfer")
    refused_feedback = models.TextField(blank=True, null=True)
    canceled_feedback = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    offer_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{}, {}'.format(self.prop, self.buyer)

    class Meta:
        verbose_name_plural = "Offers"
