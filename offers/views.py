# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from offers.models import Offer
from offers.forms import CancelOfferForm, CommentOfferForm, MakeOfferForm, RefuseOfferForm

def list_offers(request):
    cancel_offer_form = CancelOfferForm()
    comment_offer_form = CommentOfferForm()
    make_offer_form = MakeOfferForm()
    refuse_offer_form = RefuseOfferForm()

    offer_list = Offer.objects.filter(prop__user=request.user).order_by('offer_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(offer_list, 10)

    buyer_offers = Offer.objects.filter(buyer=request.user).order_by('offer_date')
    # TODO: Add pagination

    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        offers = paginator.page(1)
    except EmptyPage:
        offers = paginator.page(paginator.num_pages)

    return render(request, 'offers/offers.html', {'offers': offers, 'buyer_offers': buyer_offers,
        'cancel_offer_form': cancel_offer_form, 'comment_offer_form': comment_offer_form,
        'make_offer_form': make_offer_form, 'refuse_offer_form': refuse_offer_form})


def make_offer(request):
    if request.method == 'POST':
        form = MakeOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.buyer = request.user
            offer.save()
    else:
        pass
    return redirect('list_offers')


def accept_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    offer.status = 'accepted'
    offer.save()
    offers = Offer.objects.all().filter(prop=offer.prop).exclude(pk=offer.pk)
    for i in offers:
        i.status = 'refused'
        i.save()
    return redirect('list_offers')

# Refuse Offer

# def refuse_offer(request, pk):
#     offer = get_object_or_404(Offer, pk=pk)
#     offer.status = 'refused'
#     offer.save()
#     return True


def refuse_feedback(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = RefuseOfferForm(request.POST, instance=offer)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.status = 'refused'
            offer.save()
    else:
        pass
    return redirect('list_offers')

# Cancel Offer

# def cancel_offer(request, pk):
#     offer = get_object_or_404(Offer, pk=pk)
#     offer.status = 'canceled'
#     offer.save()
#     return redirect('list_offers')


def cancel_feedback(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = CancelOfferForm(request.POST, instance=offer)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.status = 'canceled'
            offer.save()
    else:
        pass
    return redirect('list_offers')


def comment_offer(request):
    if request.method == 'POST':
        form = CommentOfferForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        pass
    return redirect('list_offers')
