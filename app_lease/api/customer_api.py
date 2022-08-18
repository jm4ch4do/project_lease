# uses APIView

from app_lease.models import Customer
from app_lease.api.customer_serializer import CustomerSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CustomerList(APIView):
    """
    List all customers, or create a new customer.
    """

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class CustomerDetail(APIView):
    """
    Retrieve, update or delete a customer instance.
    """

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = CustomerSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = CustomerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
