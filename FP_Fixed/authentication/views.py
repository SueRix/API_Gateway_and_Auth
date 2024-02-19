from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, LogoutSerializer, ChangePasswordSerializer, UsernameChangeSerializer
from rest_framework.response import Response
from rest_framework import status


class UserRegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh']
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)
            except TokenError:
                return Response({'detail': 'Invalid token or token already blacklisted.'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeUserNameView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def patch(request):
        user = request.user
        serializer = UsernameChangeSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': "Username changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)