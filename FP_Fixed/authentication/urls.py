from django.urls import path
from .views import UserRegistrationView, LogoutView, ChangePasswordView, ChangeUserNameView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('registration', UserRegistrationView.as_view(), name='user-registration'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify', TokenVerifyView.as_view(), name='token_verify'),
    path('logout', LogoutView.as_view(), name='auth_logout'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('change-username', ChangeUserNameView.as_view(), name='change-username'),
]