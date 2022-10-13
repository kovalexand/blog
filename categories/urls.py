from rest_framework.routers import DefaultRouter
from categories import views

app_name = 'categories'
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename="category")
router.register(r'users/(?P<user_id>[^/.]+)/categories', views.UserCategoryViewSet, basename="user-category")

urlpatterns = router.urls
