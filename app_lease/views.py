from django.http import JsonResponse
from app_lease.models import Customer
from app_lease.serializers import CustomerSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def customer_list(request):

    if request.method == 'GET':

        customers = Customer.objects.all()  # get all drinks
        serializer = CustomerSerializer(customers, many=True)  # serialize them
        return JsonResponse({'customers': serializer.data})  # return json

    
