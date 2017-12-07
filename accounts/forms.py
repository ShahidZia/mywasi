# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import Profile

class SignUpForm(UserCreationForm):
    name = forms.CharField(label="Nombre y apellidos", max_length=30)
    email = forms.EmailField(max_length=256)

    class Meta:
        model = User
        fields = ('name', 'email', 'password1')
        exclude = ['username', ]

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError('Email already exists', code='invalid')
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username =  self.cleaned_data['email']
        user.first_name = self.cleaned_data['name'].split(' ')[0].capitalize()
        last_name = self.cleaned_data['name'].split(' ')
        if len(last_name) == 3:
            user.last_name = self.cleaned_data['name'].split(' ')[1].capitalize() + ' ' + self.cleaned_data['name'].split(' ')[2].capitalize()
        elif len(last_name) == 2:
            user.last_name = self.cleaned_data['name'].split(' ')[1].capitalize()
        else:
            pass

        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user',]


class StatusForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('status',)
