from app_lease.models import Customer
from rest_framework.decorators import api_view
from app_lease.api.customer_serializer import CustomerSerializer
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


@api_view(['GET', 'PUT', 'DELETE'])
def customer_edit(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify customer exists
    try:
        target_customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'response': "Customer not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user has permissions to modify
    if request.user != target_customer.user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permissions: only superuser can get another staff or superuser
    if target_user.is_staff or target_user.is_superuser:
        if not request.user.is_superuser:
            if target_user != request.user:
                return Response({'response': "No permission to access"},
                                status.HTTP_401_UNAUTHORIZED)

    # redirect to GET
    if request.method == 'GET':
        return user_edit_get(request, target_user)

    # redirect to PUT
    elif request.method == 'PUT':
        return user_edit_put(request, target_user)

    # redirect to DELETE
    elif request.method == 'DELETE':
        return user_edit_delete(request, target_user)
    pass


def user_edit_get(request, user):
    serializer = UserSerializer(user)
    return Response(serializer.data)


def user_edit_put(request, user):
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_edit_delete(request, user):
    user.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)
