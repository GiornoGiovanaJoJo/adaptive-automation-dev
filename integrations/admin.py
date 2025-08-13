from django.contrib import admin
from .models import APIIntegration, IntegrationLog, ProcessOptimization

@admin.register(APIIntegration)
class APIIntegrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'api_type', 'is_active', 'last_successful_sync', 'collection_interval']
    list_filter = ['api_type', 'is_active']
    search_fields = ['name']

    # Скрываем API ключ в админке
    readonly_fields = ['created_at', 'updated_at']

@admin.register(IntegrationLog)
class IntegrationLogAdmin(admin.ModelAdmin):
    list_display = ['integration', 'status', 'metrics_collected', 'execution_time', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['integration__name']
    date_hierarchy = 'created_at'

@admin.register(ProcessOptimization)
class ProcessOptimizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'integration', 'auto_adjustment_enabled', 'last_optimization']
    list_filter = ['auto_adjustment_enabled']
    search_fields = ['name']
