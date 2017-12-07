# -*- coding: utf-8 -*-

from django.contrib.auth import backends
from django.contrib.auth.models import User

class EmailAuthBackend(backends.ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user):
        try:
            return User.objects.get(pk=user)
        except User.DoesNotExist:
            return None
