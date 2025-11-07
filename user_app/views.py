from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from . import models
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate

@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"detail": "Email and password is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=email, password=password)
    if user is None:
        return Response(
            {"detail": "Wrong email or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
            }
        },
        status=status.HTTP_200_OK
    )
@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        print(request.user)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
        
@api_view(['POST',])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'Registration Successful'
        data['username'] = account.username
        data['email'] = account.email
  
        refresh = RefreshToken.for_user(account)
        data['token'] = {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data['errors'] = serializer.errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
