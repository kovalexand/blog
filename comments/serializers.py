from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at', 'updated_at']

    @staticmethod
    def get_author(obj):
        return obj.author.username
