from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404

from comments.paginations import CommentSetPagination
from comments.permissions import IsOwnerCommentOrReadOnly
from posts.models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer
from users.permissions import IsCurrentUserAuthenticatedOrReadOnly

UserModel = get_user_model()


class CommentViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (AllowAny, )
    lookup_url_kwarg = 'comment_id'


class PostCommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommentSetPagination
    permission_classes = (AllowAny, )
    post_lookup_url_kwarg = 'post_id'
    lookup_url_kwarg = 'comment_id'

    def get_post_object(self):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, id=self.kwargs[self.post_lookup_url_kwarg])
        return post

    def get_queryset(self):
        post = self.get_post_object()
        queryset = Comment.objects.filter(post=post)
        return queryset


class UserCommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommentSetPagination
    permission_classes = (AllowAny, )
    user_lookup_url_kwarg = 'user_id'
    lookup_url_kwarg = 'comment_id'

    def get_user_object(self):
        queryset = UserModel.objects.all()
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_queryset(self):
        user = self.get_user_object()
        queryset = Comment.objects.filter(author=user)
        return queryset


class UserPostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommentSetPagination
    permission_classes = (IsCurrentUserAuthenticatedOrReadOnly, IsOwnerCommentOrReadOnly)
    user_lookup_url_kwarg = 'user_id'
    post_lookup_url_kwarg = 'post_id'
    lookup_url_kwarg = 'comment_id'

    def get_user_object(self):
        queryset = UserModel.objects.all()
        user = get_object_or_404(queryset, id=self.kwargs[self.user_lookup_url_kwarg])
        return user

    def get_post_object(self):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, id=self.kwargs[self.post_lookup_url_kwarg])
        return post

    def get_queryset(self):
        user = self.get_user_object()
        post = self.get_post_object()
        queryset = Comment.objects.filter(author=user, post=post)
        return queryset

    def perform_create(self, serializer):
        post = self.get_post_object()
        serializer.save(author=self.request.user, post=post)
