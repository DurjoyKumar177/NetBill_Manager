from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import CustomUserRegisterSerializer, CustomUserProfileUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    permission_classes = [AllowAny]

class UpdateProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # Ensure users can only update their own profile
    
class UserTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"user_type": request.user.user_type}, status=200)