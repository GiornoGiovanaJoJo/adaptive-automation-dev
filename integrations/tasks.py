from celery import shared_task
from django.utils import timezone
import requests
import time
from .models import APIIntegration, IntegrationLog
from metrics.models import MetricSource, Metric

@shared_task
def test_api_connection(integration_id):
    """Тестирование подключения к API"""
    try:
        integration = APIIntegration.objects.get(id=integration_id)
        start_time = time.time()

        # Простой тест подключения
        headers = {
            'Authorization': f'Bearer {integration.api_key}',
            **integration.additional_headers
        }

        response = requests.get(
            integration.base_url,
            headers=headers,
            timeout=30
        )

        execution_time = time.time() - start_time

        if response.status_code == 200:
            IntegrationLog.objects.create(
                integration=integration,
                status='success',
                message=f'Подключение успешно. Status: {response.status_code}',
                execution_time=execution_time
            )
            return {'status': 'success', 'message': 'Подключение успешно'}
        else:
            IntegrationLog.objects.create(
                integration=integration,
                status='error',
                message=f'Ошибка подключения. Status: {response.status_code}',
                execution_time=execution_time
            )
            return {'status': 'error', 'message': f'HTTP {response.status_code}'}

    except Exception as e:
        IntegrationLog.objects.create(
            integration_id=integration_id,
            status='error',
            message=f'Ошибка тестирования: {str(e)}',
            execution_time=0
        )
        return {'status': 'error', 'message': str(e)}

@shared_task
def collect_metrics_from_api(integration_id):
    """Сбор метрик из внешнего API"""
    try:
        integration = APIIntegration.objects.get(id=integration_id)
        start_time = time.time()
        metrics_collected = 0

        # Получаем или создаем источник метрик
        source, created = MetricSource.objects.get_or_create(
            name=integration.name,
            defaults={
                'source_type': integration.api_type,
                'is_active': True
            }
        )

        # Собираем метрики согласно конфигурации
        for metric_config in integration.metrics_config.get('endpoints', []):
            url = f"{integration.base_url.rstrip('/')}/{metric_config['path']}"
            headers = {
                'Authorization': f'Bearer {integration.api_key}',
                **integration.additional_headers
            }

            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()

                # Извлекаем метрики из ответа
                for metric_name, json_path in metric_config.get('metrics', {}).items():
                    value = extract_json_value(data, json_path)
                    if value is not None:
                        Metric.objects.create(
                            source=source,
                            name=metric_name,
                            value=float(value),
                            unit=metric_config.get('unit', ''),
                            metadata={'integration_id': integration_id}
                        )
                        metrics_collected += 1

        execution_time = time.time() - start_time

        # Обновляем время последней синхронизации
        integration.last_successful_sync = timezone.now()
        integration.save()

        # Логируем результат
        IntegrationLog.objects.create(
            integration=integration,
            status='success',
            message=f'Собрано метрик: {metrics_collected}',
            metrics_collected=metrics_collected,
            execution_time=execution_time
        )

        return {
            'status': 'success', 
            'metrics_collected': metrics_collected,
            'execution_time': execution_time
        }

    except Exception as e:
        IntegrationLog.objects.create(
            integration_id=integration_id,
            status='error',
            message=f'Ошибка сбора метрик: {str(e)}',
            execution_time=time.time() - start_time if 'start_time' in locals() else 0
        )
        return {'status': 'error', 'message': str(e)}

def extract_json_value(data, path):
    """Извлечение значения из JSON по пути (например: 'stats.open_rate')"""
    try:
        keys = path.split('.')
        current = data
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return None

@shared_task
def collect_all_active_metrics():
    """Периодическая задача сбора всех активных метрик"""
    active_integrations = APIIntegration.objects.filter(is_active=True)

    for integration in active_integrations:
        collect_metrics_from_api.delay(integration.id)

    return f"Запущен сбор метрик для {active_integrations.count()} интеграций"
