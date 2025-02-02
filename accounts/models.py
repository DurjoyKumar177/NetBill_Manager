from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('staff', 'Staff'),
        ('user', 'User'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    isp_username = models.CharField(max_length=100, unique=True, blank=True, null=True)  
    customer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)  
    is_active = models.BooleanField(default=False) 
    location = models.CharField(max_length=255, blank=True, null=True) 
    profile_pic = models.ImageField(upload_to="accounts/profile_pics/", blank=True, null=True)  

    def save(self, *args, **kwargs):
        if self.user_type == 'staff':
            self.customer_id = None  # Ensure staff users don't require a customer ID
            self.isp_username = None  # Ensure staff users don't require an ISP username
            self.phone_number = None

        # Check for duplicate ISP usernames
        if self.isp_username and CustomUser.objects.filter(isp_username=self.isp_username).exclude(id=self.id).exists():
            raise ValidationError("A user with this ISP Username already exists.")
            
        if self.phone_number and CustomUser.objects.filter(phone_number=self.phone_number).exclude(id=self.id).exists():
            raise ValidationError("A user with this phone number already exists.")

        super().save(*args, **kwargs)
