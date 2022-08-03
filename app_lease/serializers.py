from rest_framework import serializers

from app_lease.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:

        model = Customer
        fields = ('user', 'first_name', 'last_name', 'job', 'notes',
                  'dob', 'status', 'created_at', 'updated_at', 'age', 'name')
