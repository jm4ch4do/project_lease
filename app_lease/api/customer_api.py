from app_lease.models import Customer
from rest_framework.decorators import api_view
from app_lease.api.customer_serializer import CustomerSerializer
from rest_framework import viewsets
from rest_framework import permissions
from app_lease.api.user_serializer import UserHyperSerializer, \
    UserCustomerRegSerializer, UserPasswordUpdateSerializer, LoginSerializer, \
    UserSerializer, UserAdminSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status


@api_view(['GET'])
def customer_list(request):

    # only staff and superuser can get customer list
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to view customers list"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to get customers list"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: user can't modify password if he's inactive
    if not request.user.is_active:
        return Response({'response': "No permission to get customers list"},
                        status.HTTP_401_UNAUTHORIZED)

    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)
