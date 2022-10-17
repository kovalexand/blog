from rest_framework import serializers

from categories.models import Category
from posts.serializers import PostSerializer


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'posts', 'about', 'owner', 'created_at')
