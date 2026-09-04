from django.db import models
from django.contrib.auth.models import AbstractUser


class Custom_User(AbstractUser):
    image = models.ImageField(upload_to="users/")
    phone = models.CharField(
    max_length=20,
    blank=True,
    null=True
    )
