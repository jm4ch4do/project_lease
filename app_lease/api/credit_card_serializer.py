from rest_framework import serializers
from app_lease.models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditCard
        fields = ['id', 'customer', 'name_in_card', 'provider', 'expire_month', 'expire_year',
                  'security_code', 'card_number']


class CreditCardEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditCard
        fields = ['id', 'name_in_card', 'provider', 'expire_month', 'expire_year',
                  'security_code', 'card_number']
