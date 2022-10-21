from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser

from users.permissions import IsCurrentUserAuthenticatedOrReadAndCreateOnly
from users.serializers import UserSerializer

UserModel = get_user_model()


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    parser_classes = (MultiPartParser, )
    permission_classes = (IsCurrentUserAuthenticatedOrReadAndCreateOnly, )
    lookup_url_kwarg = 'user_id'

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
