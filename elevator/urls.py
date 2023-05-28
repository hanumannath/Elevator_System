from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ElevatorViewSet, RequestViewSet

router = DefaultRouter()
router.register(r'elevators', ElevatorViewSet, basename='elevator')
router.register(r'requests', RequestViewSet, basename='elevator')

urlpatterns = router.urls