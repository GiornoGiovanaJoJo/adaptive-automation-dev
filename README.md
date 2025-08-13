# Adaptive Automation Service

Интеллектуальный сервис для автоматизации и оптимизации бизнес-процессов с помощью AI.

## Возможности
- Сбор метрик из различных источников (Mailchimp, SendGrid, CRM)
- AI-анализ данных и автоматическая оптимизация
- Веб-интерфейс для мониторинга
- Автоматическое масштабирование процессов

## Установка
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Структура проекта
- `metrics/` - работа с метриками бизнес-процессов
- `integrations/` - управление внешними API интеграциями
- `analyzer/` - AI анализ и оптимизация процессов

## Запуск Celery
```bash
# Запуск worker
celery -A adaptive_automation worker --loglevel=info

# Запуск beat (планировщик задач)
celery -A adaptive_automation beat --loglevel=info
```
