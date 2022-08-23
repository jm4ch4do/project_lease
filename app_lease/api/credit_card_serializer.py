from rest_framework import serializers
from app_lease.models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditCard
        fields = ['id', 'user', 'first_name', 'last_name', 'job', 'notes',
                  'dob', 'status', 'created_at', 'updated_at', 'age']


class CreditCardEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditCard
        fields = ['id', 'first_name', 'last_name', 'job', 'notes',
                  'dob', 'status', 'created_at', 'updated_at', 'age']
