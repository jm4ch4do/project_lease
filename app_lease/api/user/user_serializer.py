from rest_framework import serializers
from app_lease.models import Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class UserPasswordUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password']

        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def update(self, instance=None, validated_data=None):
        password = self.validated_data.get('password')
        current_user = self.instance
        current_user.set_password(password)
        current_user.save()


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Username and Password can't be empty
        if not username or not password:
            raise serializers.ValidationError("Username/password can't be empty", code='authorization')

        # False if user doesn't exist
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid username/password combination', code='authorization')

        # False if user is inactive
        if not user.is_active:
            raise serializers.ValidationError('Invalid username/password combination', code='authorization')

        # False if password doesn't match
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid username/password combination', code='authorization')



        return {'username': username, 'password': password}

    def get_token(self):
        username = self.validated_data.get('username')
        user = User.objects.get(username=username)
        token, _ = Token.objects.get_or_create(user=user)

        return token, user


class UserCustomerRegSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    job = serializers.CharField()
    notes = serializers.CharField()
    dob = serializers.DateField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2',
                  'first_name', 'last_name', 'job', 'notes', 'dob']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'job': {'required': True},
            'dob': {'required': True},
        }

    def save(self):

        email = self.validated_data.get('email')
        username = self.validated_data.get('username')
        first_name = self.validated_data.get('first_name')
        last_name = self.validated_data.get('last_name')
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')
        notes = self.validated_data.get('notes')
        dob = self.validated_data.get('dob')
        job = self.validated_data.get('job')

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        created_user = User(email=email, username=username, first_name=first_name, last_name=last_name)
        created_user.set_password(password)
        created_user.save()

        created_customer = Customer.objects.create(
            user=created_user,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            job=job,
            notes=notes,
            dob=dob,
            status=1
        )

        return created_user, created_customer
