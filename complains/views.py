from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Complain, Reply, Category
from .serializers import ComplainSerializer, ReplySerializer, CategorySerializer
from .permissions import IsOwnerOrStaff

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ComplainListCreateView(generics.ListCreateAPIView):
    serializer_class = ComplainSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 
    
    def get_queryset(self):
        if self.request.user.user_type == 'staff':
            return Complain.objects.all()  
        return Complain.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ComplainDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ComplainSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        if self.request.user.user_type == 'staff':
            return Complain.objects.all()
        return Complain.objects.filter(user=self.request.user)

class ReplyCreateView(generics.CreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 
    
    def perform_create(self, serializer):
        serializer.save(staff=self.request.user)
        
class ReplyListView(generics.ListAPIView):
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        complain_id = self.kwargs['complain_id']
        return Reply.objects.filter(complain_id=complain_id)