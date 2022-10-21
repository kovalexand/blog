from django.contrib.postgres.search import SearchVector
from django.db.models import Prefetch
from rest_framework import serializers

from categories.models import Category
from posts.models import Post
from posts.serializers import PostSerializer
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'posts', 'about', 'owner', 'created_at')

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.annotate(search=SearchVector('title')).select_related('owner').prefetch_related(
            Prefetch('posts', queryset=PostSerializer.setup_eager_loading(Post.objects.all()))
        )
