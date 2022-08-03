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
        return JsonResponse({'services': serializer.data})  # return json

    if request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request):

    if request.method == 'GET':
        pass

    elif request.method == 'PUT':
        pass

    elif request.method == 'DELETE':
        pass