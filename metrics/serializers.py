from rest_framework import serializers
from .models import MetricSource, Metric, MetricAlert

class MetricSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricSource
        fields = '__all__'

class MetricSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = Metric
        fields = '__all__'

class MetricAlertSerializer(serializers.ModelSerializer):
    metric_name = serializers.CharField(source='metric.name', read_only=True)

    class Meta:
        model = MetricAlert
        fields = '__all__'
