from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):

    # Sends an email notification when an admin activates a user account.

    if not created and instance.is_active:  # Only send if the user was just activated
        email_subject = "Your Account Has Been Activated!"
        email_body = render_to_string('activation_success_email.html', {'user': instance})

        email = EmailMultiAlternatives(email_subject, '', settings.EMAIL_HOST_USER, [instance.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()
