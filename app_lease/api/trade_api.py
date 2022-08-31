from app_lease.api.trade_serializer import TradeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app_lease.api.trade_serializer import TradeEditSerializer
from app_lease.models import Service, Trade


@api_view(['GET', 'POST'])
def trade_list(request):

    # if post redirect to create trade
    if request.method == 'POST':
        return trade_add(request)

    trades = Trade.objects.all()
    serializer = TradeSerializer(trades, many=True)
    return Response(serializer.data)


def trade_add(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to add trades"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify data is valid ('also verifies if vehicle exists')
    serializer = TradeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # verify requesting user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user has permissions to add
    target_user = serializer.validated_data['vehicle'].customer.user
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
def trade_edit(request, pk):



    # verify trade exists
    try:
        target_trade = Trade.objects.get(pk=pk)
    except Trade.DoesNotExist:
        return Response({'response': "Trade not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # redirect to GET
    if request.method == 'GET':
        return trade_edit_get(request, target_trade)

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user has permissions to modify
    if request.user != target_trade.vehicle.customer.user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # redirect to PUT
    if request.method == 'PUT':
        return vehicle_edit_put(request, target_trade)

    # redirect to DELETE
    if request.method == 'DELETE':
        return trade_edit_delete(request, target_trade)


def trade_edit_get(request, trade):
    serializer = TradeSerializer(trade)
    return Response(serializer.data)


def vehicle_edit_put(request, trade):
    serializer = TradeEditSerializer(trade, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def trade_edit_delete(request, trade):
    trade.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def trade_search(request):

    ALLOWED_FIELDS = ('note', 'status')

    parameters = request.query_params
    queryset = Trade.objects.all()

    for key, value in parameters.items():
        if key not in ALLOWED_FIELDS:
            return Response({'response': "Invalid Field " + key},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        if key == 'status':
            filter_pars = {key: int(value)}
        else:
            filter_pars = {key + '__contains': value}

        queryset = queryset.filter(**filter_pars)

    if queryset.count() == 0:
        return Response({'response': "No results found in search"},
                        status.HTTP_204_NO_CONTENT)

    serializer = TradeSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def trades_for_service(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify service exists
    try:
        target_service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({'response': "Service not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user has permissions to get
    if not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    trades = Trade.objects.filter(service_id=target_service.id)

    serializer = TradeSerializer(trades, many=True)
    return Response(serializer.data)


#  --------------------------------------------------------
# Uses Generic Class-Based api

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

# from app_lease.models import Trade
# from app_lease.api.trade_serializer import TradeSerializer
# from rest_framework import generics
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.filters import SearchFilter, OrderingFilter


# http://127.0.0.1:8000/api/trades?search=super
# http://127.0.0.1:8000/api/trades?search=1
# http://127.0.0.1:8000/api/trades?search=1&page=3
# http://127.0.0.1:8000/api/trades?search=1&ordering=-created_at

# class TradeList(generics.ListCreateAPIView):
#     queryset = Trade.objects.all()
#     serializer_class = TradeSerializer
#     # authentication_classes = (TokenAuthentication, )
#     # permission_classes = (IsAuthenticated, )
#     pagination_class = PageNumberPagination
#     filter_backends = (SearchFilter, OrderingFilter)
#     search_fields = ('status', 'vehicle__model')
#
#
# class TradeDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Trade.objects.all()
#     serializer_class = TradeSerializer
