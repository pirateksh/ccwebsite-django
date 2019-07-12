from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your models here.


class EmailBackend(object):

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            username = username.lower()
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):

        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
