from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
   followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)