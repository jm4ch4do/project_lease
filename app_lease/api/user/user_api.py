from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from app_lease.api.user.user_serializer import UserSerializer, UserCustomerRegSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = UserCustomerRegSerializer(data=request.data)
        output = {}
        if serializer.is_valid():

            # create user and customer
            created_user, created_customer = serializer.save()

            # return user data
            output['response'] = "successfully registered a new user."
            output['user_id'] = created_user.id
            output['email'] = created_user.email
            output['username'] = created_user.username
            output['customer_id'] = created_customer.id
            output['token'] = Token.objects.get(user=created_user).key

        else:
            output = serializer.errors
        return Response(output)


