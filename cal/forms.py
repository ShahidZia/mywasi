# -*- coding: utf-8 -*-

from django import forms

from cal.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'day',)
