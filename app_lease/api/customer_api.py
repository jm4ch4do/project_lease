from app_lease.models import Customer
from rest_framework.decorators import api_view
from app_lease.api.customer_serializer import CustomerSerializer, CustomerEditSerializer
from rest_framework.response import Response
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

    # redirect to GET
    if request.method == 'GET':
        return customer_edit_get(request, target_customer)

    # redirect to PUT
    elif request.method == 'PUT':
        return customer_edit_put(request, target_customer)

    # redirect to DELETE
    elif request.method == 'DELETE':
        return customer_edit_delete(request, target_customer)
    pass


def customer_edit_get(request, customer):
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)


def customer_edit_put(request, customer):
    serializer = CustomerEditSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def customer_edit_delete(request, customer):
    customer.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def customer_search(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to search users"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can access this view
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to search users"},
                        status.HTTP_401_UNAUTHORIZED)

    ALLOWED_FIELDS = ('first_name', 'last_name', 'job', 'age')

    parameters = request.query_params
    queryset = Customer.objects.filter(status=1)

    for key, value in parameters.items():
        if key not in ALLOWED_FIELDS:
            return Response({'response': "Invalid Field + key"},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        if key == 'age':
            filter_pars = {key: int(value)}
        else:
            filter_pars = {key + '__contains': value}

        queryset = queryset.filter(**filter_pars)

    if queryset.count() == 0:
        return Response({'response': "No results found in search"},
                        status.HTTP_204_NO_CONTENT)

    serializer = CustomerSerializer(queryset, many=True)
    return Response(serializer.data)
