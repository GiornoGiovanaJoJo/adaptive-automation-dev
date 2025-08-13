from rest_framework import serializers
from .models import APIIntegration, IntegrationLog, ProcessOptimization

class APIIntegrationSerializer(serializers.ModelSerializer):
    # Скрываем API ключ в ответах
    api_key = serializers.CharField(write_only=True)

    class Meta:
        model = APIIntegration
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Показываем только маскированный ключ
        data['api_key'] = f"***{instance.api_key[-4:]}" if instance.api_key else None
        return data

class IntegrationLogSerializer(serializers.ModelSerializer):
    integration_name = serializers.CharField(source='integration.name', read_only=True)

    class Meta:
        model = IntegrationLog
        fields = '__all__'

class ProcessOptimizationSerializer(serializers.ModelSerializer):
    integration_name = serializers.CharField(source='integration.name', read_only=True)

    class Meta:
        model = ProcessOptimization
        fields = '__all__'
