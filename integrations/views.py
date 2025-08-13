from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import APIIntegration, IntegrationLog, ProcessOptimization
from .serializers import APIIntegrationSerializer, IntegrationLogSerializer, ProcessOptimizationSerializer
from .tasks import test_api_connection, collect_metrics_from_api

class APIIntegrationViewSet(viewsets.ModelViewSet):
    queryset = APIIntegration.objects.all()
    serializer_class = APIIntegrationSerializer

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Тестирование подключения к API"""
        integration = self.get_object()

        # Запускаем асинхронную задачу тестирования
        task = test_api_connection.delay(integration.id)

        return Response({
            'message': 'Тестирование подключения запущено',
            'task_id': task.id
        })

    @action(detail=True, methods=['post'])
    def collect_metrics(self, request, pk=None):
        """Ручной запуск сбора метрик"""
        integration = self.get_object()

        if not integration.is_active:
            return Response(
                {'error': 'Интеграция неактивна'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Запускаем сбор метрик
        task = collect_metrics_from_api.delay(integration.id)

        return Response({
            'message': 'Сбор метрик запущен',
            'task_id': task.id
        })

class IntegrationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IntegrationLog.objects.all()
    serializer_class = IntegrationLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        integration_id = self.request.query_params.get('integration_id')
        if integration_id:
            queryset = queryset.filter(integration_id=integration_id)
        return queryset

class ProcessOptimizationViewSet(viewsets.ModelViewSet):
    queryset = ProcessOptimization.objects.all()
    serializer_class = ProcessOptimizationSerializer

    @action(detail=True, methods=['post'])
    def optimize(self, request, pk=None):
        """Запуск оптимизации процесса"""
        process = self.get_object()

        if not process.auto_adjustment_enabled:
            return Response(
                {'error': 'Автоматическая оптимизация отключена'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Здесь будет логика AI оптимизации
        # Пока просто обновляем время последней оптимизации
        process.last_optimization = timezone.now()
        process.save()

        return Response({
            'message': 'Оптимизация запущена',
            'last_optimization': process.last_optimization
        })
