from rest_framework import routers

from hairdressers import views


app_name = "hairdressers"

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'hairdressers', views.HairdresserViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = router.urls