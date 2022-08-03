from django.http import JsonResponse
from app_lease.models import Customer
from app_lease.serializers import CustomerSerializer


def customer_list(request):

    # get all drinks
    customers = Customer.objects.all()

    # serialize them
    serializer = CustomerSerializer(customers, many=True)

    # return json
    # return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'customers': serializer.data})
