from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at', 'updated_at']
        read_only_fields = ('post', )

    @staticmethod
    def get_author(obj):
        return obj.author.username
