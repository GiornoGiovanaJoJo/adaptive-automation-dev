from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AnalysisResult, OptimizationAction
from .serializers import AnalysisResultSerializer, OptimizationActionSerializer

class AnalysisResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer

    @action(detail=False, methods=['post'])
    def run_analysis(self, request):
        """Запуск нового анализа"""
        # Здесь будет логика запуска AI анализа
        return Response({'message': 'Анализ запущен'})

class OptimizationActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OptimizationAction.objects.all()
    serializer_class = OptimizationActionSerializer
