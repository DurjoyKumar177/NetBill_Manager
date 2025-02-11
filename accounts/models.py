from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


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
            self.customer_id = None
            self.isp_username = None
            self.phone_number = None
            
        if self.isp_username and CustomUser.objects.filter(isp_username=self.isp_username).exclude(id=self.id).exists():
            raise ValidationError("A user with this ISP Username already exists.")
            
        if self.phone_number and CustomUser.objects.filter(phone_number=self.phone_number).exclude(id=self.id).exists():
            raise ValidationError("A user with this phone number already exists.")

        super().save(*args, **kwargs)


class Device(models.Model):
    DEVICE_CHOICES = [
        ('tv', 'TV'),
        ('mobile', 'Mobile'),
        ('computer', 'Computer'),
        ('cctv', 'CCTV'),
        ('others', 'Others'),
    ]
    
    name = models.CharField(max_length=50, choices=DEVICE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()  # Returns the human-readable value


class AdditionalUserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="additional_info")
    customer_id = models.CharField(max_length=50, blank=True, null=True)  
    isp_username = models.CharField(max_length=100, blank=True, null=True)  
    local_area = models.CharField(max_length=255, blank=True, null=True)
    road_number = models.CharField(max_length=50, blank=True, null=True)
    building_name = models.CharField(max_length=50, blank=True, null=True)
    room_no = models.CharField(max_length=50, blank=True, null=True)

    router_model = models.CharField(max_length=100, blank=True, null=True)
    devices = models.ManyToManyField(Device, blank=True)  # Allow multiple device selections

    def __str__(self):
        return f"Additional Info for {self.user.username}"


class UserPackageInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="package_info")
    customer_id = models.CharField(max_length=50, blank=True, null=True)  
    isp_username = models.CharField(max_length=100, blank=True, null=True)  
    package_number = models.DecimalField(max_digits=1, decimal_places=0)
    package_password = models.CharField(max_length=255)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    package_slip = models.FileField(upload_to="packages/slips/", blank=True, null=True)

    def __str__(self):
        return f"Package Info for {self.user.username}"


# Signal to auto-create AdditionalUserInfo and UserPackageInfo when a new user is created
@receiver(post_save, sender=CustomUser)
def create_related_user_info(sender, instance, created, **kwargs):
    if created and instance.user_type == 'user':
        AdditionalUserInfo.objects.create(user=instance, customer_id=instance.customer_id, isp_username=instance.isp_username)
        UserPackageInfo.objects.create(user=instance, customer_id=instance.customer_id, isp_username=instance.isp_username)

@receiver(post_save, sender=CustomUser)
def save_related_user_info(sender, instance, **kwargs):
    if instance.user_type == 'user':
        instance.additional_info.customer_id = instance.customer_id
        instance.additional_info.isp_username = instance.isp_username
        instance.additional_info.save()

        instance.package_info.customer_id = instance.customer_id
        instance.package_info.isp_username = instance.isp_username
        instance.package_info.save()
