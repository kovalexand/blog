from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from blog import settings


class User(AbstractUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=15, validators=[username_validator])
    email = models.EmailField(db_index=True, unique=True)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT+'/users', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username
