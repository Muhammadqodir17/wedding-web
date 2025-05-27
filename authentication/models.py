from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class BlacklistedAccessToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.blacklisted_at}'
