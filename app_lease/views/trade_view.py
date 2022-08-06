# Uses Generic Class-Based views

from app_lease.models import Trade
from app_lease.serializers import TradeSerializer
from rest_framework import generics


class TradeList(generics.ListCreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
