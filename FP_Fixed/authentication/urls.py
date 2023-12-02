from django.urls import path
from .views import UserRegistrationView, RefreshTokenView
from .views import CustomLoginView

urlpatterns = [
    path('registration', UserRegistrationView.as_view(), name='user-registration'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('refresh', RefreshTokenView.as_view(), name='refresh-token'),
]
