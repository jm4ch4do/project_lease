from rest_framework import serializers
from app_lease.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:

        model = Vehicle
        fields = ('id', 'customer', 'make_model', 'make', 'model', 'category',
                  'machine_make_model', 'machine_make', 'machine_model',
                  'machine_category', 'year', 'machine_year')


class VehicleEditSerializer(serializers.ModelSerializer):

    class Meta:

        model = Vehicle
        fields = ('id', 'make_model', 'make', 'model', 'category',
                  'machine_make_model', 'machine_make', 'machine_model',
                  'machine_category', 'year', 'machine_year')
