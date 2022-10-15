from rest_framework.routers import DefaultRouter
from comments import views

app_name = "comments"
routers = DefaultRouter()
routers.register(r'comments', views.CommentViewSet, basename='comment')
routers.register(r'users/(?P<user_id>[^/.]+)/comments', views.UserCommentViewSet, basename='user-comment')
routers.register(r'posts/(?P<post_id>[^/.]+)/comments', views.PostCommentViewSet, basename='post-comment')
routers.register(
    r'users/(?P<user_id>[^/.]+)/posts/(?P<post_id>[^/.]+)/posts',
    views.UserPostCommentViewSet, basename='user-post-comment'
)

urlpatterns = routers.urls
