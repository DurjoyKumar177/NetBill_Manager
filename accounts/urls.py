from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView
from .views import RegisterUserView, UpdateProfileView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),  # Custom User Registration
    path('auth/', include('dj_rest_auth.urls')),  # Login, Logout, Password Reset, Change Password
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration endpoints
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('auth/token/login/', LoginView.as_view(), name='token_login'),  # Login with Token
    path('auth/token/logout/', LogoutView.as_view(), name='token_logout'),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),  # Get Token after login
]

