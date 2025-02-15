from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Device

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):

    if created:
        Token.objects.create(user=instance)

@receiver(post_migrate)
def populate_devices(sender, **kwargs):

    if sender.name == "accounts": 
        device_choices = [
            ('tv', 'TV'),
            ('mobile', 'Mobile'),
            ('computer', 'Computer'),
            ('cctv', 'CCTV'),
            ('others', 'Others'),
        ]
        for code, name in device_choices:
            Device.objects.get_or_create(name=code)