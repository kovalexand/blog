from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404

from posts.paginations import PostSetPagination
from posts.permissions import IsOwnerPostOrReadOnly
from users.permissions import IsCurrentUserAuthenticatedOrReadOnly
from categories.models import Category
from posts.models import Post
from posts.serializers import PostSerializer

UserModel = get_user_model()


class PostViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        queryset = self.get_serializer().setup_eager_loading(self.queryset)
        return queryset


class CategoryPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostSetPagination
    permission_classes = (AllowAny, )
    category_lookup_url_kwarg = 'category_id'
    lookup_url_kwarg = 'post_id'

    def get_category_object(self):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, id=self.kwargs[self.category_lookup_url_kwarg])
        return category

    def get_queryset(self):
        category = self.get_category_object()
        queryset = self.get_serializer().setup_eager_loading(self.queryset)
        return queryset.filter(category=category)


class UserPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostSetPagination
    permission_classes = (AllowAny, )
    user_lookup_url_kwarg = 'user_id'
    lookup_url_kwarg = 'post_id'

    def get_user_object(self):
        queryset = UserModel.objects.all()
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_queryset(self):
        user = self.get_user_object()
        queryset = self.get_serializer().setup_eager_loading(self.queryset)
        return queryset.filter(owner=user)


class UserCategoryPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostSetPagination
    permission_classes = (IsCurrentUserAuthenticatedOrReadOnly, IsOwnerPostOrReadOnly)
    user_lookup_url_kwarg = 'user_id'
    category_lookup_url_kwarg = 'category_id'
    lookup_url_kwarg = 'post_id'

    def get_user_object(self):
        queryset = UserModel.objects.all()
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_category_object(self):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, id=self.kwargs[self.category_lookup_url_kwarg])
        return category

    def get_queryset(self):
        user = self.get_user_object()
        category = self.get_category_object()
        queryset = self.get_serializer().setup_eager_loading(self.queryset)
        return queryset.filter(owner=user, category=category)

    def perform_create(self, serializer):
        category = self.get_category_object()
        serializer.save(owner=self.request.user, category=category)
