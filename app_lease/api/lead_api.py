# Uses Generic Class-Based api

from app_lease.models import Lead
from app_lease.serializers import LeadSerializer
from rest_framework import generics


class LeadList(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
