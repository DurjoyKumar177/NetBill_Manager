from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Announcement Model
class Announcement(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, related_name='announcements')
    title = models.CharField(max_length=255, blank=True, null=True) 
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title if self.title else "Untitled Announcement"


# Announcement Media Model (For Multiple Images/Videos)
class AnnouncementMedia(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='media')
    media_file = models.FileField(upload_to='announcement/media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.announcement.creator.username}'s Announcement"

# Comment Model
class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.announcement}"

# Reaction Model
class Reaction(models.Model):
    REACTION_CHOICES = [
        ("like", "👍"),
        ("love", "❤️"),
        ("haha", "😂"),
        ("wow", "😮"),
        ("sad", "😢"),
        ("angry", "😡"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'announcement')  # One reaction per user per announcement
    
    def __str__(self):
        return f"{self.user.username} reacted {self.reaction} to {self.announcement}"
