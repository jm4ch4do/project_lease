from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from app_lease.api.user_serializer import UserHyperSerializer, \
    UserCustomerRegSerializer, UserPasswordUpdateSerializer, LoginSerializer, \
    UserSerializer, UserAdminSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserHyperSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def user_register(request):
    """ User registers creating user and customer and getting token back """

    status_code = status.HTTP_201_CREATED
    serializer = UserCustomerRegSerializer(data=request.data)
    output = {}
    if serializer.is_valid():

        # create user and customer
        created_user, created_customer = serializer.save()

        # return user data
        output['response'] = "successfully registered a new user."
        output['user_id'] = created_user.id
        output['email'] = created_user.email
        output['username'] = created_user.username
        output['customer_id'] = created_customer.id
        output['token'] = Token.objects.get(user=created_user).key

    else:
        output = serializer.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(output, status=status_code)


@api_view(['PUT'])
def user_password_update(request, pk):
    """ Allow change user password """

    # verify user exists
    try:
        target_user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'response': "User not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to change password"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user has permissions to modify
    if request.user != target_user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to modify the user's password"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: only superuser can modify superuser
    if target_user.is_superuser and not request.user.is_superuser:
        return Response({'response': "No permission to modify the user's password"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: user can't modify password if he's inactive
    if not request.user.is_active:
        return Response({'response': "No permission to modify the user's password"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify data is valid
    serializer = UserPasswordUpdateSerializer(target_user, data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    # update password
    serializer.update()

    # return response
    return Response({'response': "Password Updated"}, status.HTTP_200_OK)


@api_view(['POST'])
def user_login(request):
    """ User logs in and gets token back """

    # load data into serializer
    login_serializer = LoginSerializer(data=request.data)

    # data validation
    if not login_serializer.is_valid():
        return Response(login_serializer.errors, status.HTTP_400_BAD_REQUEST)

    # get token
    token, user = login_serializer.get_token()
    output = {'response': "successful login",
              'username': user.username,
              'token': token.key}

    # return
    return Response(output, status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def user_list(request):

    # if post redirect to create user
    if request.method == 'POST':
        return user_add(request)

    # only staff and superuser can get user list
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to view users list"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to get users list"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permission: user can't modify password if he's inactive
    if not request.user.is_active:
        return Response({'response': "No permission to get users list"},
                        status.HTTP_401_UNAUTHORIZED)

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_search(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to search users"},
                        status.HTTP_401_UNAUTHORIZED)

    # only staff and superuser can access this view
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'response': "No permission to search users"},
                        status.HTTP_401_UNAUTHORIZED)

    ALLOWED_FIELDS = ('username', 'first_name', 'last_name')

    parameters = request.query_params
    queryset = User.objects.filter(is_active=True)

    for key, value in parameters.items():
        if key not in ALLOWED_FIELDS:
            return Response({'response': "Invalid Field " + key},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)
        filter_pars = {key + '__contains': value}
        queryset = queryset.filter(**filter_pars)

    if queryset.count() == 0:
        return Response({'response': "No results found in search"},
                        status.HTTP_204_NO_CONTENT)

    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def user_add(request):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Logging to be able to add users"},
                        status.HTTP_401_UNAUTHORIZED)

    # only superuser can create user (you can also register users for regular users)
    if not request.user.is_superuser:
        return Response({'response': "No permission to add users"},
                        status.HTTP_401_UNAUTHORIZED)

    serializer = UserAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_edit(request, pk):

    # verify user is authenticated
    if not request.user.is_authenticated:
        return Response({'response': "Please logging before proceeding"},
                        status.HTTP_401_UNAUTHORIZED)

    # verify user exists
    try:
        target_user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'response': "User not Found"},
                        status=status.HTTP_404_NOT_FOUND)

    # verify user has permissions to modify
    if request.user != target_user and \
        not request.user.is_staff and \
            not request.user.is_superuser:

        return Response({'response': "No permission to access"},
                        status.HTTP_401_UNAUTHORIZED)

    # extra permissions: only superuser can get another staff or superuser
    if target_user.is_staff or target_user.is_superuser:
        if not request.user.is_superuser:
            if target_user != request.user:
                return Response({'response': "No permission to access"},
                                status.HTTP_401_UNAUTHORIZED)

    # redirect to GET
    if request.method == 'GET':
        return user_edit_get(request, target_user)

    # redirect to PUT
    elif request.method == 'PUT':
        return user_edit_put(request, target_user)

    # redirect to DELETE
    elif request.method == 'DELETE':
        return user_edit_delete(request, target_user)
    pass


def user_edit_get(request, user):
    serializer = UserSerializer(user)
    return Response(serializer.data)


def user_edit_put(request, user):
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_edit_delete(request, user):
    user.delete()
    return Response({'response': "Remove Completed"}, status=status.HTTP_204_NO_CONTENT)
