from app_lease.serializers import TradeSerializer
from rest_framework import serializers
from app_lease.models import Service


class ServiceAdminSerializer(serializers.ModelSerializer):

    trades = TradeSerializer(source='trade_set', many=True, read_only=True)

    class Meta:

        model = Service
        fields = ('id', 'name', 'cost', 'description', 'when_to_pay', 'service_type', 'trades')


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Service
        fields = ('id', 'name', 'cost', 'description', 'when_to_pay', 'service_type')
