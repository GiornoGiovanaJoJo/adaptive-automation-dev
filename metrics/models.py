from django.db import models
from django.contrib.auth.models import User

class MetricSource(models.Model):
    """Источник метрик"""
    name = models.CharField(max_length=100, verbose_name="Название")
    source_type = models.CharField(max_length=50, choices=[
        ('mailchimp', 'Mailchimp'),
        ('sendgrid', 'SendGrid'),
        ('crm', 'CRM System'),
        ('support', 'Support System'),
        ('simulator', 'Data Simulator'),
    ], verbose_name="Тип источника")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Источник метрик"
        verbose_name_plural = "Источники метрик"

    def __str__(self):
        return self.name

class Metric(models.Model):
    """Метрика бизнес-процесса"""
    source = models.ForeignKey(MetricSource, on_delete=models.CASCADE, verbose_name="Источник")
    name = models.CharField(max_length=100, verbose_name="Название метрики")
    value = models.FloatField(verbose_name="Значение")
    unit = models.CharField(max_length=50, verbose_name="Единица измерения", blank=True)
    metadata = models.JSONField(default=dict, verbose_name="Дополнительные данные")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время сбора")

    class Meta:
        verbose_name = "Метрика"
        verbose_name_plural = "Метрики"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.name}: {self.value} {self.unit}"

class MetricAlert(models.Model):
    """Уведомления о критических изменениях метрик"""
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50, choices=[
        ('threshold', 'Превышение порога'),
        ('anomaly', 'Аномалия'),
        ('trend', 'Негативный тренд'),
    ])
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ['-created_at']
