from rest_framework import serializers
from app_lease.models import Service, Lead, Vehicle, Trade
from django.contrib.auth.models import Group


class TradeSerializer(serializers.ModelSerializer):

    vehicle_name = serializers.CharField(source='vehicle.name')
    vehicle_model = serializers.CharField(source='vehicle.model')

    class Meta:

        model = Trade
        fields = ('id', 'service', 'vehicle', 'note', 'status', 'created_at',
                  'updated_at', 'label', 'vehicle', 'vehicle_name', 'vehicle_model')


class ServiceSerializer(serializers.ModelSerializer):

    trades = TradeSerializer(source='trade_set', many=True, read_only=True)

    class Meta:

        model = Service
        fields = ('id', 'name', 'cost', 'description', 'when_to_pay', 'service_type', 'trades')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:

        model = Vehicle
        fields = ('id', 'customer', 'make_model', 'make', 'model', 'category',
                  'machine_make_model', 'machine_make', 'machine_model',
                  'machine_category', 'year', 'machine_year', 'created_at', 'updated_at')


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'first_name', 'last_name', 'source', 'notes',
                  'dob', 'created_at', 'updated_at', 'name']




