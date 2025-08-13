from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MetricSourceViewSet, MetricViewSet, MetricAlertViewSet

router = DefaultRouter()
router.register(r'sources', MetricSourceViewSet)
router.register(r'data', MetricViewSet)
router.register(r'alerts', MetricAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
