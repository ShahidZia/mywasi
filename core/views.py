# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core.forms import ValuationForm
from accounts.forms import UserForm, ProfileForm
from properties.models import Document

def home(request):
    return render(request, 'landingpage.html', {})


def pricing(request):
    return render(request, 'core/pricing.html', {})


def documents(request):
    documents = Document.objects.all().filter(prop__user=request.user.pk)
    return render(request, 'core/documents.html', {'documents': documents})


def valuation(request):
    if request.method == 'POST':
        form = ValuationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_activation_sent')

    else:
        form = ValuationForm()
    return render(request, 'core/valuation.html', {'form': form})
