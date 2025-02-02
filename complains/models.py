from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Complain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complains')
    title = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='complains')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class ComplainAttachment(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='complains/complain_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.complain.title}"

class Reply(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE, related_name='replies')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.complain.title} by {self.staff.username}"

class ReplyAttachment(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='complains/reply_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for reply to {self.reply.complain.title}"
