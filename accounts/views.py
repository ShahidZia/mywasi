# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail

from accounts.forms import SignUpForm, UserForm, ProfileForm, StatusForm
from accounts.tokens import account_activation_token
from accounts.models import Profile


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            message = render_to_string('accounts/registration/account_activation_email.html', {
                'user': user,
                'domain': 'mywasi.com',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail('Verify your Mywasi account', message, 'hello@himynameismik.com', [user.email])

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'accounts/registration/account_activation_sent.html', {})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('properties')
    else:
        return render(request, 'accounts/registration/account_activation_invalid.html', {})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada!')
            return redirect('password_change')
        else:
            messages.error(request, 'Por favor, corrija los errores.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/registration/password_change_form.html', {'form': form})


@login_required
def edit_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, user=request.user.pk)
    if request.method == 'POST':
        uform = UserForm(request.POST, instance=user)
        pform = ProfileForm(request.POST, request.FILES, instance=profile)

        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            profile = pform.save(commit=False)
            profile.user = user
            profile.save()
    else:
        uform = UserForm(instance=user)
        pform = ProfileForm(instance=profile)
    return render(request, 'dashboard/settings.html', {'uform': uform, 'pform': pform})


def change_user_status(request, status):
    user = get_object_or_404(User, pk=request.user.pk)
    user.profile.status = status
    user.save()
    return redirect('properties')


@login_required
def search_for_users(request):

    query = request.GET.get('term')
    if query and request.is_ajax():
        suggestions = Profile.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(user__email__icontains=query) | Q(phone__icontains=query), user__is_superuser=False).exclude(user_id=request.user.id)
        if suggestions.exists():
            context = {
                'profiles': suggestions,
                'term': query,
            }
            return render_to_response('chat/partials/suggestions.html', context)

    return HttpResponse('')