from django.db import models
from django.core.validators import URLValidator

class APIIntegration(models.Model):
    """Интеграция с внешним API"""
    name = models.CharField(max_length=100, verbose_name="Название интеграции")
    api_type = models.CharField(max_length=50, choices=[
        ('mailchimp', 'Mailchimp'),
        ('sendgrid', 'SendGrid'),
        ('hubspot', 'HubSpot CRM'),
        ('zendesk', 'Zendesk Support'),
        ('custom', 'Custom API'),
    ], verbose_name="Тип API")

    base_url = models.URLField(verbose_name="Базовый URL API")
    api_key = models.CharField(max_length=255, verbose_name="API ключ")
    additional_headers = models.JSONField(
        default=dict, 
        verbose_name="Дополнительные заголовки",
        help_text="JSON объект с дополнительными HTTP заголовками"
    )

    # Конфигурация метрик для сбора
    metrics_config = models.JSONField(
        default=dict,
        verbose_name="Конфигурация метрик",
        help_text="JSON с настройками эндпоинтов и параметров для сбора метрик"
    )

    # Настройки расписания
    collection_interval = models.IntegerField(
        default=300, 
        verbose_name="Интервал сбора (секунды)",
        help_text="Как часто собирать метрики с этого API"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активна")
    last_successful_sync = models.DateTimeField(null=True, blank=True, verbose_name="Последняя синхронизация")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "API Интеграция"
        verbose_name_plural = "API Интеграции"

    def __str__(self):
        return f"{self.name} ({self.api_type})"

class IntegrationLog(models.Model):
    """Логи выполнения интеграций"""
    integration = models.ForeignKey(APIIntegration, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('success', 'Успешно'),
        ('error', 'Ошибка'),
        ('timeout', 'Таймаут'),
    ])
    message = models.TextField(verbose_name="Сообщение")
    metrics_collected = models.IntegerField(default=0, verbose_name="Собрано метрик")
    execution_time = models.FloatField(verbose_name="Время выполнения (сек)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Лог интеграции"
        verbose_name_plural = "Логи интеграций"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.integration.name} - {self.status} - {self.created_at}"

class ProcessOptimization(models.Model):
    """Настройки оптимизации процессов"""
    name = models.CharField(max_length=100, verbose_name="Название процесса")
    integration = models.ForeignKey(
        APIIntegration, 
        on_delete=models.CASCADE,
        verbose_name="Связанная интеграция"
    )

    # Параметры для оптимизации
    optimization_rules = models.JSONField(
        default=dict,
        verbose_name="Правила оптимизации",
        help_text="JSON с правилами автоматической настройки"
    )

    # Текущие настройки процесса
    current_settings = models.JSONField(
        default=dict,
        verbose_name="Текущие настройки"
    )

    # AI может их менять
    auto_adjustment_enabled = models.BooleanField(
        default=True, 
        verbose_name="Автоматическая подстройка"
    )

    last_optimization = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Оптимизация процесса"
        verbose_name_plural = "Оптимизации процессов"

    def __str__(self):
        return self.name
