from rest_framework import serializers
from app_lease.models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contact
        fields = ('id', 'customer', 'lead', 'phone', 'email', 'note', 'type')

    def validate(self, data):
        instance = Contact(**data)
        instance.clean()
        return data


class ContactEditSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contact
        fields = ('id', 'phone', 'email', 'note', 'type')
