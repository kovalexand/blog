from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404

from users.permissions import IsCurrentUserAuthenticated
from categories.models import Category
from categories.serializers import CategorySerializer

UserModel = get_user_model()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('posts', 'posts__comments').filter(owner__is_active=True)
    permission_classes = (AllowAny, )
    lookup_url_kwarg = 'category_id'


class UserCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    SAFE_ACTIONS = ['retrieve', 'list']
    user_lookup_url_kwarg = 'user_id'
    lookup_url_kwarg = 'category_id'

    def get_user_object(self):
        queryset = UserModel.objects.filter(is_active=True)
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_permissions(self):
        permission_classes = [AllowAny, ]
        if self.action not in self.SAFE_ACTIONS:
            permission_classes.append(IsCurrentUserAuthenticated)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.get_user_object()
        queryset = Category.objects.prefetch_related('posts', 'posts__comments').filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        user = self.get_user_object()
        serializer.save(owner=user)
