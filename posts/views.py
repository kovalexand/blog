from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404

from users.permissions import IsCurrentUserAuthenticated
from categories.models import Category
from posts.models import Post
from posts.serializers import PostSerializer

UserModel = get_user_model()


class PostViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.prefetch_related('comments').filter(owner__is_active=True)
    permission_classes = (AllowAny, )
    lookup_url_kwarg = 'post_id'


class CategoryPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )
    category_lookup_url_kwarg = 'category_id'
    lookup_url_kwarg = 'post_id'

    def get_category_object(self):
        queryset = Category.objects.prefetch_related('posts', 'posts__comments').filter(owner__is_active=True)
        category = get_object_or_404(queryset, id=self.kwargs[self.category_lookup_url_kwarg])
        return category

    def get_queryset(self):
        category = self.get_category_object()
        queryset = Post.objects.prefetch_related('comments').filter(category=category, owner__is_active=True)
        return queryset


class UserPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )
    user_lookup_url_kwarg = 'user_id'
    lookup_url_kwarg = 'post_id'

    def get_user_object(self):
        queryset = UserModel.objects.filter(is_active=True)
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_queryset(self):
        user = self.get_user_object()
        queryset = Post.objects.prefetch_related('comments').filter(owner=user)
        return queryset


class UserCategoryPostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    user_lookup_url_kwarg = 'user_id'
    category_lookup_url_kwarg = 'category_id'
    lookup_url_kwarg = 'post_id'
    SAFE_ACTIONS = ['retrieve', 'list']

    def get_permissions(self):
        permission_classes = [AllowAny, ]
        if self.action not in self.SAFE_ACTIONS:
            permission_classes.append(IsCurrentUserAuthenticated)
        return [permission() for permission in permission_classes]

    def get_user_object(self):
        queryset = UserModel.objects.filter(is_active=True)
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_category_object(self):
        queryset = Category.objects.prefetch_related('posts', 'posts__comments').filter(owner__is_active=True)
        category = get_object_or_404(queryset, id=self.kwargs[self.category_lookup_url_kwarg])
        return category

    def get_queryset(self):
        user = self.get_user_object()
        category = self.get_category_object()
        queryset = Post.objects.prefetch_related('comments').filter(owner=user, category=category)
        return queryset

    def perform_create(self, serializer):
        user = self.get_user_object()
        category = self.get_category_object()
        serializer.save(owner=user, category=category)
