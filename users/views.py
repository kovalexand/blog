from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser

from users.permissions import IsCurrentUserAuthenticated
from users.serializers import UserSerializer

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.filter(is_active=True)
    parser_classes = (MultiPartParser, )
    SAFE_ACTIONS = ('create', 'list', 'retrieve')

    def get_permissions(self):
        permission_classes = [AllowAny, ]
        if self.action not in self.SAFE_ACTIONS:
            permission_classes.append(IsCurrentUserAuthenticated)
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
