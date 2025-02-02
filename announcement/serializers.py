from rest_framework import serializers
from .models import Announcement, AnnouncementMedia, Comment, Reaction

class AnnouncementMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementMedia
        fields = ['id', 'media_file', 'uploaded_at']

class AnnouncementSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    media = AnnouncementMediaSerializer(many=True, read_only=True)  # Include media in response
    media_files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )  # Accept multiple files during creation

    class Meta:
        model = Announcement
        fields = ['id', 'creator', 'title', 'text', 'created_at', 'updated_at', 'media', 'media_files']

    def create(self, validated_data):
        media_files = validated_data.pop('media_files', []) 
        announcement = Announcement.objects.create(**validated_data)

        # Save media files
        for media_file in media_files:
            AnnouncementMedia.objects.create(announcement=announcement, media_file=media_file)

        return announcement

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()
    
    class Meta:
        model = Reaction
        fields = '__all__'
