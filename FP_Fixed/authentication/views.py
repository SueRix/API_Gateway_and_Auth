from rest_framework.generics import CreateAPIView

from .serializers import RegistrationSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer


# class CustomLoginView(APIView):
#     @staticmethod
#     def post(request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         validated_data = serializer.validated_data
#         user = authenticate(email=validated_data['email'], password=validated_data['password'])
#         if not user:
#             return HttpResponseBadRequest('Invalid credentials or user does not exist.')
#
#         access_token = generate_access_token(user)
#         refresh_token = generate_refresh_token(user)
#
#         return Response({
#             'accessToken': access_token,
#             'refreshToken': refresh_token
#         }, status=status.HTTP_200_OK)
#
#
# class RefreshTokenView(APIView):
#     @staticmethod
#     def post(request):
#         serializer = RefreshTokenSerializer(data=request.data)
#         if serializer.is_valid():
#             new_access_token = serializer.get_new_access_token()
#             return Response({'access': new_access_token}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
