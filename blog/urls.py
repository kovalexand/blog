from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from blog import settings
from categories.views import CategoryViewSet, UserCategoryViewSet
from comments.views import CommentViewSet, UserCommentViewSet, PostCommentViewSet, UserPostCommentViewSet
from posts.views import PostViewSet, UserPostViewSet, CategoryPostViewSet, UserCategoryPostViewSet
from users.views import UserViewSet

users = DefaultRouter()
users.register(r'users', UserViewSet, basename='user')

categories = DefaultRouter()
categories.register(r'categories', CategoryViewSet, basename="category")
categories.register(r'users/(?P<user_id>[^/.]+)/categories', UserCategoryViewSet, basename="user-category")

posts = DefaultRouter()
posts.register(r'posts', PostViewSet, basename='post')
posts.register(r'users/(?P<user_id>[^/.]+)/posts', UserPostViewSet, basename='user-post')
posts.register(r'categories/(?P<category_id>[^/.]+)/posts', CategoryPostViewSet, basename='category-post')
posts.register(
    r'users/(?P<user_id>[^/.]+)/categories/(?P<category_id>[^/.]+)/posts',
    UserCategoryPostViewSet, basename='user-category-post'
)

comments = DefaultRouter()
comments.register(r'comments', CommentViewSet, basename='comment')
comments.register(r'users/(?P<user_id>[^/.]+)/comments', UserCommentViewSet, basename='user-comment')
comments.register(r'posts/(?P<post_id>[^/.]+)/comments', PostCommentViewSet, basename='post-comment')
comments.register(
    r'users/(?P<user_id>[^/.]+)/posts/(?P<post_id>[^/.]+)/posts',
    UserPostCommentViewSet, basename='user-post-comment'
)

media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path(r'api/', include((users.urls, 'users'), namespace='users')),
    path(r'api/', include((categories.urls, 'categories'), namespace='categories')),
    path(r'api/', include((posts.urls, 'posts'), namespace='posts')),
    path(r'api/', include((comments.urls, 'comments'), namespace='comments')),
    path(r'auth/refresh/', TokenRefreshView.as_view()),
    path(r'auth/login/', TokenObtainPairView.as_view())
] + static_urls + media_urls
