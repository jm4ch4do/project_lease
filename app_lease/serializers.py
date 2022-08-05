from rest_framework import serializers
from app_lease.models import Service, Customer
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


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'job', 'notes',
                  'dob', 'status', 'created_at', 'updated_at', 'age']
