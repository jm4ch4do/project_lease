from django.http import JsonResponse
from app_lease.models import Service
from app_lease.serializers import ServiceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# ----------------------------------- SERVICES ----------------------------------- #
@api_view(['GET', 'POST'])
def service_list(request):

    if request.method == 'GET':
        return service_list_get(request)

    if request.method == 'POST':
        return service_list_post(request)


def service_list_get(request):
    services = Service.objects.all()  # get all drinks
    serializer = ServiceSerializer(services, many=True)  # serialize them
    return Response(serializer.data)
    # return JsonResponse({'services': serializer.data})  # return json


def service_list_post(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------- SERVICE ----------------------------------- #
@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request, pk):

    # ----- verify service exists
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # ----- Get service detail
    if request.method == 'GET':
        return service_detail_get(request, service)

    # ----- Modify service
    elif request.method == 'PUT':
        return service_detail_put(request, service)

    # ----- Delete service
    elif request.method == 'DELETE':
        return service_detail_delete(request, service)


def service_detail_get(request, service):
    serializer = ServiceSerializer(service)
    return Response(serializer.data)


def service_detail_put(request, service):
    serializer = ServiceSerializer(service, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def service_detail_delete(request, service):
    service.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
