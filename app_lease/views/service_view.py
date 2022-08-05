from django.http import JsonResponse
from app_lease.models import Service
from app_lease.serializers import ServiceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def service_list(request):

    if request.method == 'GET':

        services = Service.objects.all()  # get all drinks
        serializer = ServiceSerializer(services, many=True)  # serialize them
        return Response(serializer.data)
        # return JsonResponse({'services': serializer.data})  # return json

    if request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request, id):

    # ----- verify service exists
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # ----- Get service detail
    if request.method == 'GET':
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    # ----- Modify service
    elif request.method == 'PUT':
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    # ----- Delete service
    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
