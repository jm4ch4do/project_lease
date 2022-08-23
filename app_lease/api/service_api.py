from app_lease.models import Service
from rest_framework.decorators import api_view
from app_lease.api.service_serializer import ServiceSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def service_list(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to get vehicle list"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: can't access if user's inactive
    if not request.user.is_active:
        return Response({'response': "User not found or inactive"},
                        status.HTTP_404_NOT_FOUND)

    # if requests is post -> redirect to create service
    if request.method == 'POST':
        return service_add(request)

    # if request is get -> return list of services
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


def service_add(request):

    # only staff and superuser can access this view
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to add service"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify data is valid
    serializer = ServiceSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # save data and response ok
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def service_edit(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to get vehicle list"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can edit
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to view/edit services list"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: can't access if user's inactive
    if not request.user.is_active:
        return Response({'response': "No permission to view/edit services list"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify service exists
    try:
        target_service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({'response': "Service not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # redirect to GET
    if request.method == 'GET':
        return service_edit_get(request, target_service)

    # redirect to PUT
    elif request.method == 'PUT':
        return service_edit_put(request, target_service)

    # redirect to DELETE
    elif request.method == 'DELETE':
        return service_edit_delete(request, target_service)
    pass


def service_edit_get(request, service):
    serializer = ServiceSerializer(service)
    return Response(serializer.data)


def service_edit_put(request, service):
    serializer = ServiceSerializer(service, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def service_edit_delete(request, service):
    service.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def service_search(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to search services"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can access this view
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to search services"},
                        status.HTTP_401_UNAUTHORIZED)

    ALLOWED_FIELDS = ('id', 'name', 'cost', 'when_to_pay', 'service_type')

    parameters = request.query_params
    queryset = Service.objects.all()

    for key, value in parameters.items():
        if key not in ALLOWED_FIELDS:
            return Response({'response': "Invalid Field + key"},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        if key == 'cost':
            filter_pars = {key: float(value)}
        elif key == 'when_to_pay' or key == 'service_type':
            filter_pars = {key: int(value)}
        else:
            filter_pars = {key + '__contains': value}

        queryset = queryset.filter(**filter_pars)

    if queryset.count() == 0:
        return Response({'response': "No results found in search"},
                        status.HTTP_204_NO_CONTENT)

    serializer = ServiceSerializer(queryset, many=True)
    return Response(serializer.data)
