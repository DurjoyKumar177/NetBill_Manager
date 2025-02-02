from django.urls import path, include
from .views import RegisterUserView, UpdateProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),  # Custom User Registration
    path('auth/', include('dj_rest_auth.urls')),  # Login, Logout, Password Reset, Change Password
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration endpoints
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
]

