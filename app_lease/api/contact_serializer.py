from rest_framework import serializers
from app_lease.models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contact
        fields = ('id', 'customer', 'lead', 'phone', 'email', 'note', 'type')


class ContactEditSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contact
        fields = ('id', 'phone', 'email', 'note', 'type')
