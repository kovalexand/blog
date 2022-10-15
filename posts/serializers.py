from rest_framework import serializers

from comments.serializers import CommentSerializer
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = CommentSerializer(write_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'comments', 'content', 'owner', 'category', 'created_at')
