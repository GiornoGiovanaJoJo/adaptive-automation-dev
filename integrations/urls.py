from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIIntegrationViewSet, IntegrationLogViewSet, ProcessOptimizationViewSet

router = DefaultRouter()
router.register(r'api', APIIntegrationViewSet)
router.register(r'logs', IntegrationLogViewSet)
router.register(r'optimizations', ProcessOptimizationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
