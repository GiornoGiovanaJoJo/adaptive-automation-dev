from rest_framework import serializers
from .models import AnalysisResult, OptimizationAction

class AnalysisResultSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = AnalysisResult
        fields = '__all__'

class OptimizationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimizationAction
        fields = '__all__'
