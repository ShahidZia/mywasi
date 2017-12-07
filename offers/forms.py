# -*- coding: utf-8 -*-

from django import forms

from offers.models import Offer

class MakeOfferForm(forms.ModelForm):
    # Choices = Properties that user likes
    class Meta:
        model = Offer
        fields = ('prop', 'amount', 'payment_type',)


class RefuseOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('refused_feedback',)


class CancelOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('canceled_feedback',)


class CommentOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('comment',)
