from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalysisResultViewSet, OptimizationActionViewSet

router = DefaultRouter()
router.register(r'results', AnalysisResultViewSet)
router.register(r'actions', OptimizationActionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
