from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(email=username)
#         except User.DoesNotExist:
#             return None
#
#         if user.check_password(password):
#             return user
#
#         return None

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=username) | Q(phone_number=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
