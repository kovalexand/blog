from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404

from categories.paginations import CategorySetPagination
from categories.permissions import IsOwnerCategoryOrReadOnly
from users.permissions import IsCurrentUserAuthenticatedOrReadOnly
from categories.models import Category
from categories.serializers import CategorySerializer

UserModel = get_user_model()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategorySetPagination
    permission_classes = (AllowAny, )
    lookup_url_kwarg = 'category_id'
    search_query_param = 'q'

    def get_queryset(self):
        queryset = self.get_serializer().setup_eager_loading(self.queryset)
        search_query = self.request.query_params.get(self.search_query_param, None)
        return queryset.filter(search=search_query) if search_query else queryset


class UserCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategorySetPagination
    permission_classes = (IsCurrentUserAuthenticatedOrReadOnly, IsOwnerCategoryOrReadOnly)
    user_lookup_url_kwarg = 'user_id'
    lookup_url_kwarg = 'category_id'

    def get_user_object(self):
        queryset = UserModel.objects.all()
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_queryset(self):
        user = self.get_user_object()
        queryset = self.get_serializer().setup_eager_loading(self.queryset)
        return queryset.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
