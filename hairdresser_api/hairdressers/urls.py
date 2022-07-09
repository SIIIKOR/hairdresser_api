from django.urls import path

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from hairdressers import views


app_name = "hairdressers"

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'hairdressers', views.HairdresserViewSet)
router.register(r'orders', views.OrderViewSet, basename="order")

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('register/', views.RegisterView.as_view(), name='register-api'),
]
urlpatterns += router.urls