
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('api/', include('users.urls', namespace='users')),
]
