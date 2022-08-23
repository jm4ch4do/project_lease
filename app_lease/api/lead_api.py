from app_lease.models import Lead
from rest_framework.decorators import api_view
from app_lease.api.lead_serializer import LeadSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def lead_list(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to get vehicle list"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can get lead list or create lead
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to view/create leads list"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: can't access if user's inactive
    if not request.user.is_active:
        return Response({'response': "User not found or inactive"},
                        status.HTTP_404_NOT_FOUND)

    # if requests is post -> redirect to create lead
    if request.method == 'POST':
        return lead_add(request)

    # if request is get -> return list of leads
    leads = Lead.objects.all()
    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)


def lead_add(request):

    # verify data is valid
    serializer = LeadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # save data and response ok
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def lead_edit(request, pk):

# verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to get vehicle list"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can get lead list or create lead
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to view/create leads list"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: can't access if user's inactive
    if not request.user.is_active:
        return Response({'response': "No permission to view/create leads list"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify lead exists
    try:
        target_lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({'response': "Lead not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # redirect to GET
    if request.method == 'GET':
        return lead_edit_get(request, target_lead)

    # redirect to PUT
    elif request.method == 'PUT':
        return lead_edit_put(request, target_lead)

    # redirect to DELETE
    elif request.method == 'DELETE':
        return lead_edit_delete(request, target_lead)
    pass


def lead_edit_get(request, lead):
    serializer = LeadSerializer(lead)
    return Response(serializer.data)


def lead_edit_put(request, lead):
    serializer = LeadSerializer(lead, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def lead_edit_delete(request, lead):
    lead.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def lead_search(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to search lead"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can access this view
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to search leads"},
                        status.HTTP_401_UNAUTHORIZED)

    ALLOWED_FIELDS = ('id', 'first_name', 'last_name', 'source', 'notes')

    parameters = request.query_params
    queryset = Lead.objects.all()

    for key, value in parameters.items():
        if key not in ALLOWED_FIELDS:
            return Response({'response': "Invalid Field + key"},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        filter_pars = {key + '__contains': value}
        queryset = queryset.filter(**filter_pars)

    if queryset.count() == 0:
        return Response({'response': "No results found in search"},
                        status.HTTP_204_NO_CONTENT)

    serializer = LeadSerializer(queryset, many=True)
    return Response(serializer.data)
