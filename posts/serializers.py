from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'owner', 'category', 'created_at')
