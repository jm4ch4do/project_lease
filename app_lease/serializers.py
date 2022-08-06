from rest_framework import serializers
from app_lease.models import Service, Customer, Lead, Vehicle, Trade
from django.contrib.auth.models import User, Group


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Service
        fields = ('id', 'name', 'cost', 'description', 'when_to_pay', 'service_type')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


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


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'job', 'notes',
                  'dob', 'status', 'created_at', 'updated_at', 'age']


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'first_name', 'last_name', 'source', 'notes',
                  'dob', 'created_at', 'updated_at', 'name']


class TradeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Trade
        fields = ('id', 'service', 'vehicle', 'note', 'status', 'created_at',
                  'updated_at', 'label')

