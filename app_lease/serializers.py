from rest_framework import serializers

from app_lease.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:

        model = Service
        fields = ('name', 'cost', 'description', 'when_to_pay', 'service_type')
