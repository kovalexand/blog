from rest_framework import serializers

from comments.serializers import CommentSerializer
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'comments', 'content', 'owner', 'category', 'created_at')
        read_only_fields = ('owner', 'category')

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.prefetch_related('comments')
