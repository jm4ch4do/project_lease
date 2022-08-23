from rest_framework import serializers
from app_lease.models import Service, Trade
from django.contrib.auth.models import Group


class TradeSerializer(serializers.ModelSerializer):

    vehicle_name = serializers.CharField(source='vehicle.name')
    vehicle_model = serializers.CharField(source='vehicle.model')

    class Meta:

        model = Trade
        fields = ('id', 'service', 'vehicle', 'note', 'status', 'created_at',
                  'updated_at', 'label', 'vehicle', 'vehicle_name', 'vehicle_model')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
