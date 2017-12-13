# -*- coding: utf-8 -*-
import datetime
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _

from accounts.models import Profile


class Dialog(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"), related_name="selfDialogs")
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog opponent"))

    def __str__(self):
        return _("Chat with ") + self.opponent.username


class Message(TimeStampedModel, SoftDeletableModel):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Dialog"), related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages")
    text = models.TextField(verbose_name=_("Message text"))
    read = models.BooleanField(verbose_name=_("Read"), default=False)
    all_objects = models.Manager()
    kind = models.IntegerField(default=0, blank=True)

    def get_formatted_create_datetime(self):
        dateMsg = datetime.datetime.date(self.created)
        dateNow = datetime.datetime.now()

        fstr = "H:m"

        if dateNow.day is not dateMsg.day:
            fstr = "d/m/y"

        return dj_date(self.created, fstr)

    def my_get_formatted_create_datetime(self):
        return dj_date(self.created, "d M")

    def sender_photo(self):
        profile = Profile.objects.get(user=self.sender)
        if profile.image:
            return profile.image.url
        else:
            return False

    def __str__(self):
        return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"
