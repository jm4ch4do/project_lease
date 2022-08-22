from app_lease.models import Vehicle
from rest_framework.decorators import api_view
from app_lease.api.vehicle_serializer import VehicleSerializer, VehicleEditSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def vehicle_list(request):

    # only staff and superuser can get vehicle list
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to view vehicle list"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to get vehicle list"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: user can't modify password if he's inactive
    if not request.user.is_active:
        return Response({'response': "No permission to get vehicle list"},
                        status.HTTP_401_UNAUTHORIZED)

    vehicles = Vehicle.objects.all()
    serializer = VehicleSerializer(vehicles, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def vehicle_edit(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify vehicle exists
    try:
        target_vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        return Response({'response': "Vehicle not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user has permissions to modify
    if request.user != target_vehicle.customer.user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # redirect to GET
    if request.method == 'GET':
        return vehicle_edit_get(request, target_vehicle)

    # redirect to PUT
    elif request.method == 'PUT':
        return vehicle_edit_put(request, target_vehicle)

    # redirect to DELETE
    elif request.method == 'DELETE':
        return vehicle_edit_delete(request, target_vehicle)
    pass


def vehicle_edit_get(request, vehicle):
    serializer = VehicleSerializer(vehicle)
    return Response(serializer.data)


def vehicle_edit_put(request, vehicle):
    serializer = VehicleEditSerializer(vehicle, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def vehicle_edit_delete(request, vehicle):
    vehicle.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def vehicle_search(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to search vehicles"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can access this view
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to search vehicles"},
                        status.HTTP_401_UNAUTHORIZED)

    ALLOWED_FIELDS = ('make_model', 'make', 'model', 'category',
                      'machine_make_model', 'machine_make', 'machine_model',
                      'machine_category', 'year', 'machine_year')

    parameters = request.query_params
    queryset = Vehicle.objects.all()

    for key, value in parameters.items():
        if key not in ALLOWED_FIELDS:
            return Response({'response': "Invalid Field + key"},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        if key == 'year':
            filter_pars = {key: int(value)}
        else:
            filter_pars = {key + '__contains': value}

        queryset = queryset.filter(**filter_pars)

    if queryset.count() == 0:
        return Response({'response': "No results found in search"},
                        status.HTTP_204_NO_CONTENT)

    serializer = VehicleSerializer(queryset, many=True)
    return Response(serializer.data)
