from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from blog import settings
from blog.settings import DEBUG
from blog.yasg import url_patterns as doc_urls
from categories.views import CategoryViewSet, UserCategoryViewSet
from comments.views import CommentViewSet, UserCommentViewSet, PostCommentViewSet, UserPostCommentViewSet
from posts.views import PostViewSet, UserPostViewSet, CategoryPostViewSet, UserCategoryPostViewSet
from users.views import UserViewSet

routers = DefaultRouter()
routers.register(r'users', UserViewSet, basename='user')

routers.register(r'categories', CategoryViewSet, basename="category")
routers.register(r'users/(?P<user_id>[^/.]+)/categories', UserCategoryViewSet, basename="user-category")

routers.register(r'posts', PostViewSet, basename='post')
routers.register(r'users/(?P<user_id>[^/.]+)/posts', UserPostViewSet, basename='user-post')
routers.register(r'categories/(?P<category_id>[^/.]+)/posts', CategoryPostViewSet, basename='category-post')
routers.register(
    r'users/(?P<user_id>[^/.]+)/categories/(?P<category_id>[^/.]+)/posts',
    UserCategoryPostViewSet, basename='user-category-post'
)

routers.register(r'comments', CommentViewSet, basename='comment')
routers.register(r'users/(?P<user_id>[^/.]+)/comments', UserCommentViewSet, basename='user-comment')
routers.register(r'posts/(?P<post_id>[^/.]+)/comments', PostCommentViewSet, basename='post-comment')
routers.register(
    r'users/(?P<user_id>[^/.]+)/posts/(?P<post_id>[^/.]+)/posts',
    UserPostCommentViewSet, basename='user-post-comment'
)

media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path(r'api/', include(routers.urls)),
    path(r'auth/refresh/', TokenRefreshView.as_view()),
    path(r'auth/login/', TokenObtainPairView.as_view(), name='login')
]

urlpatterns += doc_urls

if DEBUG:
    urlpatterns += static_urls + media_urls
