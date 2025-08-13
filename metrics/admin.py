from django.contrib import admin
from .models import MetricSource, Metric, MetricAlert

@admin.register(MetricSource)
class MetricSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'is_active', 'created_at']
    list_filter = ['source_type', 'is_active']
    search_fields = ['name']

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'source', 'value', 'unit', 'timestamp']
    list_filter = ['source', 'timestamp']
    search_fields = ['name']
    date_hierarchy = 'timestamp'

@admin.register(MetricAlert)
class MetricAlertAdmin(admin.ModelAdmin):
    list_display = ['metric', 'alert_type', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'is_resolved']
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_resolved.short_description = "Пометить как решенные"
