from rest_framework.routers import DefaultRouter
from posts import views

app_name = "posts"
routers = DefaultRouter()
routers.register(r'posts', views.PostViewSet, basename='post')
routers.register(r'users/(?P<user_id>[^/.]+)/posts', views.UserPostViewSet, basename='user-post')
routers.register(r'categories/(?P<category_id>[^/.]+)/posts', views.CategoryPostViewSet, basename='category-post')
routers.register(
    r'users/(?P<user_id>[^/.]+)/categories/(?P<category_id>[^/.]+)/posts',
    views.UserCategoryPostViewSet, basename='user-category-post'
)

urlpatterns = routers.urls
