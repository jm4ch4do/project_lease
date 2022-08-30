from app_lease.models import Contact, Customer, Lead
from rest_framework.decorators import api_view
from app_lease.api.contact_serializer import ContactSerializer, ContactEditSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def contact_list(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to proceed"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # if post redirect to create contact
    if request.method == 'POST':
        return contact_add(request)

    # for staff or superuser load full contact list
    if request.user.is_staff or request.user.is_superuser:
        vehicles = Contact.objects.all()

    # for regular customer load only customer contacts
    else:
        customer = request.user.customer
        vehicles = Contact.objects.filter(customer=customer)

    # error if no vehicles found
    if not vehicles:
        return Response({'response': "No contacts found"},
                        status.HTTP_204_NO_CONTENT)

    # return results
    serializer = ContactSerializer(vehicles, many=True)
    return Response(serializer.data)


def contact_add(request):

    # verify data is valid (also checks for customer or lead must exist)
    serializer = ContactSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # load related values
    target_customer = serializer.validated_data['customer']
    target_lead = serializer.validated_data['lead']

    # lead_contact can only be created by staff or superuser
    if target_lead is not None:
        if not request.user.is_staff and \
                not request.user.is_superuser:

            return Response({'response': "No permission to add contacts for leads"},
                            status.HTTP_401_UNAUTHORIZED)

    # customer_contact can be added by own customer or staff or superuser
    if target_customer is not None:
        if not request.user.is_staff and \
                not request.user.is_superuser and \
                target_customer.user != request.user:

            return Response({'response': "No permission to add contacts for this customer"},
                            status.HTTP_401_UNAUTHORIZED)

    # save data and response ok
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def contact_edit(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify contact exists
    try:
        target_contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response({'response': "Vehicle not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # lead_contact can only be modified by staff or superuser
    if target_contact.lead is not None:
        if not request.user.is_staff and \
                not request.user.is_superuser:

            return Response({'response': "No permission to modify contact for a lead"},
                            status.HTTP_401_UNAUTHORIZED)

    # customer_contact can be modified by own customer or staff or superuser
    if target_contact.customer is not None:
        if not request.user.is_staff and \
                not request.user.is_superuser and \
                target_contact.customer.user != request.user:

            return Response({'response': "No permission to modify contact for this customer"},
                            status.HTTP_401_UNAUTHORIZED)

    # redirect to GET
    if request.method == 'GET':
        return contact_edit_get(request, target_contact)

    # redirect to PUT
    elif request.method == 'PUT':
        return contact_edit_put(request, target_contact)

    # redirect to DELETE
    elif request.method == 'DELETE':
        return contact_edit_delete(request, target_contact)
    pass


def contact_edit_get(request, contact):
    serializer = ContactSerializer(contact)
    return Response(serializer.data)


def contact_edit_put(request, contact):
    serializer = ContactEditSerializer(contact, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def contact_edit_delete(request, contact):
    contact.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def contact_search(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to search vehicles"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can access this view
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to search contacts"},
                        status.HTTP_401_UNAUTHORIZED)

    ALLOWED_FIELDS = ('phone', 'email', 'note', 'type')

    parameters = request.query_params
    queryset = Contact.objects.all()

    for key, value in parameters.items():
        if key not in ALLOWED_FIELDS:
            return Response({'response': "Invalid Field + key"},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        if key == 'type':
            filter_pars = {key: int(value)}
        else:
            filter_pars = {key + '__contains': value}

        queryset = queryset.filter(**filter_pars)

    if queryset.count() == 0:
        return Response({'response': "No results found in search"},
                        status.HTTP_204_NO_CONTENT)

    serializer = ContactSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def contacts_for_customer(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify customer exists
    try:
        target_customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'response': "Customer not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user has permissions to get
    if request.user != target_customer.user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    vehicles = Contact.objects.filter(customer_id=target_customer.id)

    serializer = ContactSerializer(vehicles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def contacts_for_lead(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is active
    if not request.user.is_active:
        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify customer exists
    try:
        target_customer = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({'response': "Lead not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user has permissions to get
    if not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    vehicles = Contact.objects.filter(lead_id=target_customer.id)

    serializer = ContactSerializer(vehicles, many=True)
    return Response(serializer.data)
