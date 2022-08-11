from rest_framework import serializers
from app_lease.models import Service, Customer, Lead, Vehicle, Trade
from django.contrib.auth.models import User, Group


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


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class UserRegSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def save(self):

        email = self.validated_data.get('email')
        username = self.validated_data.get('username')
        first_name = self.validated_data.get('first_name')
        last_name = self.validated_data.get('last_name')
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        created_user = User(email=email, username=username, first_name=first_name, last_name=last_name)
        created_user.set_password(password)
        created_user.save()
        return created_user


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




