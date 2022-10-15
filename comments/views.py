from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404

from posts.models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer
from users.permissions import IsCurrentUserAuthenticated

UserModel = get_user_model()


class CommentViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer()
    queryset = Comment.objects.filter(author__is_active=True)
    permission_classes = (AllowAny, )


class PostCommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer()
    permission_classes = (AllowAny, )
    post_lookup_url_kwarg = 'post_id'

    def get_post_object(self):
        queryset = Post.objects.filter(owner__is_active=True)
        post = get_object_or_404(queryset, id=self.kwargs[self.post_lookup_url_kwarg])
        return post

    def get_queryset(self):
        post = self.get_post_object()
        queryset = Comment.objects.filter(post=post)
        return queryset


class UserCommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny, )
    user_lookup_url_kwarg = 'user_id'

    def get_user_object(self):
        queryset = UserModel.objects.filter(is_active=True)
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_queryset(self):
        user = self.get_user_object()
        queryset = Comment.objects.filter(owner=user)
        return queryset


class UserPostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    user_lookup_url_kwarg = 'user_id'
    post_lookup_url_kwarg = 'post_id'
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

    def get_post_object(self):
        queryset = Post.objects.filter(owner__is_active=True)
        post = get_object_or_404(queryset, id=self.kwargs[self.post_lookup_url_kwarg])
        return post

    def get_queryset(self):
        user = self.get_user_object()
        post = self.get_post_object()
        queryset = Comment.objects.filter(owner=user, post=post)
        return queryset

    def perform_create(self, serializer):
        user = self.get_user_object()
        post = self.get_post_object()
        serializer.save(owner=user, post=post)
