from urllib import request
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, generics
from rest_framework.response import Response


from .serializer import ChangePasswordSerializer

from .models import User
from datetime import datetime


# Create your views here.

# login user

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def userlogin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
    #  user = auth.authenticate(username=username, password=password)
    user = authenticate(request=request, email=email, password=password)

    if user is not None:
        login(request, user)

    # user = authenticate(email=email, password=password)
    print(user)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    user.last_login = datetime.now()
    user.save()
    return Response({'user_id': user.pk,
                     'email': user.email,
                     'token': {token.key}
                     }, status=status.HTTP_200_OK)

#


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def create(request):
    email = str(request.data.get('email'))
    password = str(request.data.get('password'))
    username = str(request.data.get('username'))

    user = User.objects.create_user(email, password, username)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': {token.key}}, status=status.HTTP_200_OK)


# Change paspword
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_passwword": ["Wrong password ."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
