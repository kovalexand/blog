from django.contrib.auth import get_user_model
from django.db import models

from posts.models import Post

UserModel = get_user_model()


class Comment(models.Model):
    content = models.TextField(max_length=100)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
