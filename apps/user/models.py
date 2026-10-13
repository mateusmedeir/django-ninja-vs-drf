import secrets

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.user.choices import UserLevel


class User(AbstractUser):
    level = models.CharField(max_length=20, choices=UserLevel.choices, blank=True)
    tertiarygroup = models.ForeignKey(
        'group.TertiaryGroup', on_delete=models.PROTECT, null=True, blank=True, related_name='users'
    )
    regional = models.ForeignKey(
        'group.Regional', on_delete=models.PROTECT, null=True, blank=True, related_name='users'
    )


def generate_token_key():
    return secrets.token_hex(20)


class AccessToken(models.Model):
    key = models.CharField(max_length=40, unique=True, default=generate_token_key)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_token'
    )
    created_at = models.DateTimeField(auto_now_add=True)
