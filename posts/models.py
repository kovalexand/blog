from django.contrib.auth import get_user_model
from django.db import models

from categories.models import Category

UserModel = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=50, unique=True)
    content = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
