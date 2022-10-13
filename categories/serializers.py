from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'about', 'owner', 'created_at')
