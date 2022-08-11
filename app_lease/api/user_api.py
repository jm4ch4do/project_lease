from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from app_lease.serializers import UserSerializer, UserRegSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = UserRegSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = user.email
            data['username'] = user.username
            data['token'] = Token.objects.get(user=user).key
        else:
            data = serializer.errors
        return Response(data)


# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         username = request.data["username"]
#         password = request.data["password"]
#
#         user = User.objects.filter(username=username).first()
#
#         # wrong user or password
#         if not user or not user.check_password(raw_password=password):
#             return Response("Invalid Credentials", status=status.HTTP_404_NOT_FOUND)
#
#         token = create_token(user_id=user.id)
#
#         response
