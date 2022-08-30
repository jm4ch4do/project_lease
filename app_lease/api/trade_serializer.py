from rest_framework import serializers
from app_lease.models import Trade


class TradeSerializer(serializers.ModelSerializer):

    vehicle_name = serializers.CharField(source='vehicle.name', required=False, read_only=True)
    vehicle_model = serializers.CharField(source='vehicle.model', required=False, read_only=True)

    class Meta:

        model = Trade
        fields = ('id', 'service', 'vehicle', 'note', 'status', 'created_at',
                  'updated_at', 'label', 'vehicle_name', 'vehicle_model')

class TradeEditSerializer(serializers.ModelSerializer):

    class Meta:

        model = Trade
        fields = ('id', 'note', 'status')
