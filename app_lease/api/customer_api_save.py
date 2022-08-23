# uses APIView

from app_lease.models import Customer
from app_lease.api.customer_serializer import CustomerSerializer
from django.http import Http404
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import UserPassesTestMixin


class StaffOrSuperUserOnlyMixin(UserPassesTestMixin, APIView):

    def test_func(self):

        user = self.request.user
        return True if user.is_superuser or user.is_staff else False

    def handle_no_permission(self):
        return JsonResponse({'response': "No permission to access"}, status=status.HTTP_401_UNAUTHORIZED)


class CustomerList(StaffOrSuperUserOnlyMixin, APIView):
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
