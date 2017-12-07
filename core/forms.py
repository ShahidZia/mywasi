# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail

from core.models import Valuation
from accounts.tokens import account_activation_token

class ValuationForm(forms.ModelForm):
    email = forms.EmailField(label='Email*', max_length=256, required=True)
    password1 = forms.CharField(label='Password*', widget=forms.PasswordInput(), required=True)
    user_name = forms.CharField(label='Nombre y apellidos', max_length=256, required=False)
    phone = forms.CharField(label='Movil*', max_length=10, required=True)

    class Meta:
        model = Valuation
        fields = ('user_name', 'phone', 'email', 'password1', 'location', 'number', 'prop', 'prop_type')
        exclude = ['user', ]
        labels = {
            'location': 'Calle y población (SIN NÚMERO)',
            'number': 'Número de Edificio',
            'prop': 'Inmueble',
            'prop_type': 'Tipo de Inmueble',
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError('El email ya existe', code='invalid')
        return email

    def save(self, commit=True):
        valuation = super(ValuationForm, self).save(commit=False)

        user = User.objects.create_user(username=self.cleaned_data['email'], password=self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['user_name'].split(' ')[0]
        last_name = self.cleaned_data['user_name'].split(' ')
        if len(last_name) == 3:
            user.last_name = self.cleaned_data['user_name'].split(' ')[1].capitalize() + ' ' + self.cleaned_data['user_name'].split(' ')[2].capitalize()
        elif len(last_name) == 2:
            user.last_name = self.cleaned_data['user_name'].split(' ')[1].capitalize()
        else:
            pass

        user.email = self.cleaned_data['email']
        user.profile.phone = self.cleaned_data['phone']
        user.is_active = False
        user.save()

        message = render_to_string('accounts/registration/account_activation_email.html', {
            'user': user,
            'domain': 'mywasi.com',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail('Verify your Mywasi account', message, 'hello@himynameismik.com', [user.email])

        if commit:
            valuation.user = user
            valuation.save()
        return valuation
