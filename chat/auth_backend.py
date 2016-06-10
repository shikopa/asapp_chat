from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class AuthenticationBackend(ModelBackend):

    def authenticate(self, **credentials):
        username = credentials["username"]

        users= User.objects.filter(username__iexact=username)
        if users:
            return users[0]

        user = User.objects.create_user(username=username)
        return user

EmailModelBackend = AuthenticationBackend