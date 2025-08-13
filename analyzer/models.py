from django.db import models
from metrics.models import Metric, MetricSource

class AnalysisResult(models.Model):
    """Результаты AI анализа метрик"""
    source = models.ForeignKey(MetricSource, on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=50, choices=[
        ('trend', 'Анализ трендов'),
        ('anomaly', 'Обнаружение аномалий'),
        ('optimization', 'Рекомендации по оптимизации'),
        ('forecast', 'Прогнозирование'),
    ])

    # Результаты анализа
    findings = models.JSONField(verbose_name="Результаты анализа")
    confidence_score = models.FloatField(verbose_name="Уровень уверенности")

    # Рекомендации
    recommendations = models.JSONField(default=list, verbose_name="Рекомендации")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Результат анализа"
        verbose_name_plural = "Результаты анализа"
        ordering = ['-created_at']

class OptimizationAction(models.Model):
    """Действия по оптимизации, выполненные AI"""
    analysis_result = models.ForeignKey(AnalysisResult, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    description = models.TextField()
    parameters_changed = models.JSONField(default=dict)

    status = models.CharField(max_length=20, choices=[
        ('pending', 'Ожидает'),
        ('applied', 'Применено'),
        ('failed', 'Ошибка'),
    ], default='pending')

    applied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Действие оптимизации"
        verbose_name_plural = "Действия оптимизации"
