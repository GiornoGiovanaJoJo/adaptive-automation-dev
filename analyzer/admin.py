from django.contrib import admin
from .models import AnalysisResult, OptimizationAction

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['source', 'analysis_type', 'confidence_score', 'created_at']
    list_filter = ['analysis_type', 'created_at']
    search_fields = ['source__name']

@admin.register(OptimizationAction)
class OptimizationActionAdmin(admin.ModelAdmin):
    list_display = ['analysis_result', 'action_type', 'status', 'applied_at']
    list_filter = ['status', 'action_type']
