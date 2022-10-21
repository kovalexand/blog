from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'image', 'password', 'created_at', 'is_active')
        read_only_fields = ('is_active', )

    def create(self, validated_data):
        model = self.Meta.model
        instance = model.objects.create_user(**validated_data)
        return instance
