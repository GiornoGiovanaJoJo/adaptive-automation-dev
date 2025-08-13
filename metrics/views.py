from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from .models import MetricSource, Metric, MetricAlert
from .serializers import MetricSourceSerializer, MetricSerializer, MetricAlertSerializer

class MetricSourceViewSet(viewsets.ModelViewSet):
    queryset = MetricSource.objects.all()
    serializer_class = MetricSourceSerializer

class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Данные для дашборда"""
        now = timezone.now()
        last_24h = now - timedelta(hours=24)

        # Собираем статистику за последние 24 часа
        recent_metrics = Metric.objects.filter(timestamp__gte=last_24h)

        dashboard_data = {
            'total_metrics': recent_metrics.count(),
            'active_sources': MetricSource.objects.filter(is_active=True).count(),
            'alerts_count': MetricAlert.objects.filter(is_resolved=False).count(),
            'avg_values_by_source': list(
                recent_metrics.values('source__name')
                .annotate(avg_value=Avg('value'), count=Count('id'))
            ),
            'recent_alerts': MetricAlertSerializer(
                MetricAlert.objects.filter(is_resolved=False)[:5], many=True
            ).data
        }

        return Response(dashboard_data)

class MetricAlertViewSet(viewsets.ModelViewSet):
    queryset = MetricAlert.objects.all()
    serializer_class = MetricAlertSerializer

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Пометить уведомление как решенное"""
        alert = self.get_object()
        alert.is_resolved = True
        alert.save()
        return Response({'status': 'resolved'})
