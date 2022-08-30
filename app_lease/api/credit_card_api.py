from app_lease.models import CreditCard, Customer
from rest_framework.decorators import api_view
from app_lease.api.credit_card_serializer import CreditCardSerializer, CreditCardEditSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def credit_card_list(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to get vehicle list"},
                        status.HTTP_401_UNAUTHORIZED)

    # if post redirect to create credit card
    if request.method == 'POST':
        return credit_card_add(request)

    # only staff and superuser can get credit card list
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to view credit card list"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: reject inactive user
    if not request.user.is_active:
        return Response({'response': "No permission to get credit card list"},
                        status.HTTP_401_UNAUTHORIZED)

    vehicles = CreditCard.objects.all()
    serializer = CreditCardSerializer(vehicles, many=True)
    return Response(serializer.data)


def credit_card_add(request):

    # verify data is valid ('also verifies if customer exists')
    serializer = CreditCardSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # verify requesting user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user has permissions to add
    target_user = serializer.validated_data['customer'].user
    if request.user != target_user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify target user is active
    if not target_user.is_active:
        return Response({'response': "Target user is not active or does not exists"},
                        status.HTTP_404_NOT_FOUND)

    # save data and response ok
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def credit_card_edit(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify credit card exists
    try:
        target_credit_card = CreditCard.objects.get(pk=pk)
    except CreditCard.DoesNotExist:
        return Response({'response': "Credit Card not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user has permissions to modify
    if request.user != target_credit_card.customer.user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # redirect to GET
    if request.method == 'GET':
        return credit_card_edit_get(request, target_credit_card)

    # redirect to PUT
    elif request.method == 'PUT':
        return credit_card_edit_put(request, target_credit_card)

    # redirect to DELETE
    elif request.method == 'DELETE':
        return credit_card_edit_delete(request, target_credit_card)
    pass


def credit_card_edit_get(request, credit_card):
    serializer = CreditCardSerializer(credit_card)
    return Response(serializer.data)


def credit_card_edit_put(request, credit_card):
    serializer = CreditCardEditSerializer(credit_card, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def credit_card_edit_delete(request, credit_card):
    credit_card.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def credit_card_search(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to search credit cards"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can access this view
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to search credit cards"},
                        status.HTTP_401_UNAUTHORIZED)

    ALLOWED_FIELDS = ('name_in_card', 'expire_month', 'expire_year', 'last_four_digits')

    parameters = request.query_params
    queryset = CreditCard.objects.all()

    for key, value in parameters.items():
        if key not in ALLOWED_FIELDS:
            return Response({'response': "Invalid Field + key"},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        if key == 'expire_month' or key == 'expire_year':
            filter_pars = {key: int(value)}
        else:
            filter_pars = {key + '__contains': value}

        queryset = queryset.filter(**filter_pars)

    if queryset.count() == 0:
        return Response({'response': "No results found in search"},
                        status.HTTP_204_NO_CONTENT)

    serializer = CreditCardSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def credit_cards_for_customer(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify customer exists
    try:
        target_customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'response': "Customer not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user has permissions to get
    if request.user != target_customer.user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    vehicles = CreditCard.objects.filter(customer_id=target_customer.id)

    serializer = CreditCardSerializer(vehicles, many=True)
    return Response(serializer.data)
