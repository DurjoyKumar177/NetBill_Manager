from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Announcement, AnnouncementMedia, Comment, Reaction
from .serializers import AnnouncementSerializer, AnnouncementMediaSerializer, CommentSerializer, ReactionSerializer
from .permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly, IsCommentOwnerOrReadOnly


# Announcement Views
class AnnouncementListCreateView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [IsStaffOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]  # Allow file uploads

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff users can create announcements.")
        serializer.save(creator=self.request.user)


class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
# Media Upload View (Allows adding media separately)
class AnnouncementMediaUploadView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, announcement_id):
        announcement = get_object_or_404(Announcement, id=announcement_id)
        
        if announcement.creator != request.user:
            raise PermissionDenied("You can only add media to your own announcements.")
        
        files = request.FILES.getlist('media_files')
        media_objects = [AnnouncementMedia(announcement=announcement, media_file=file) for file in files]
        AnnouncementMedia.objects.bulk_create(media_objects)
        
        return Response({"message": "Media uploaded successfully."})


# Comment Views
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwnerOrReadOnly]


# Reaction Views
class ReactionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, announcement_id):
        announcement = get_object_or_404(Announcement, id=announcement_id)
        reaction_type = request.data.get("reaction")

        # Check if user has already reacted
        existing_reaction = Reaction.objects.filter(user=request.user, announcement=announcement).first()
        
        if existing_reaction:
            if existing_reaction.reaction == reaction_type:
                existing_reaction.delete()
                return Response({"message": "Reaction removed."})
            else:
                existing_reaction.reaction = reaction_type
                existing_reaction.save()
                return Response({"message": "Reaction updated."})

        # Create new reaction
        Reaction.objects.create(user=request.user, announcement=announcement, reaction=reaction_type)
        return Response({"message": "Reaction added."})


class ReactionListView(generics.ListAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        announcement_id = self.kwargs['announcement_id']
        return Reaction.objects.filter(announcement_id=announcement_id)
