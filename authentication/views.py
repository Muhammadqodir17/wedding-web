from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import (
    AccessToken,
    RefreshToken
)
from .models import User, BlacklistedAccessToken
from .serializers import LogoutSerializer


class LoginViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The username",
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The user's password.",
                ),
            },
            required=['username', 'password'],
        ),
        responses={200: 'Success'},
        operation_summary="Log in a user",
        operation_description='Log in a user',
        tags=['auth']
    )
    def login_user(self, request):
        data = request.data
        user = User.objects.filter(username=data.get('username')).first()
        if user is None:
            return Response(data={'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(data.get('password')):
            return Response(data={'error': 'Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['role'] = 'admin'
        return Response(data={'refresh': str(refresh_token), 'access_token': str(access_token)},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Access_token')
            }
        ),
        responses={
            205: 'Token has been added to blacklist',
            400: 'Refresh token not provided'
        },
        operation_summary="User logout",
        operation_description="This endpoint allows a user to log out.",
        tags=['auth']
    )
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'error': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = serializer.validated_data['refresh_token']
        access_token = serializer.validated_data['access_token']
        token1 = RefreshToken(refresh_token)
        token2 = AccessToken(access_token)
        token1.blacklist()
        obj = BlacklistedAccessToken.objects.create(token=token2)
        obj.save()
        return Response(data={'message': 'Logged out successfully', 'ok': True},
                        status=status.HTTP_205_RESET_CONTENT)