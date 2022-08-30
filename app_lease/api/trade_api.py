# Uses Generic Class-Based api

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

from app_lease.models import Trade
from app_lease.api.trade_serializer import TradeSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter


# http://127.0.0.1:8000/api/trades?search=super
# http://127.0.0.1:8000/api/trades?search=1
# http://127.0.0.1:8000/api/trades?search=1&page=3
# http://127.0.0.1:8000/api/trades?search=1&ordering=-created_at

class TradeList(generics.ListCreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('status', 'vehicle__model')


class TradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
