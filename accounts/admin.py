from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "user_type", "phone_number", "is_active") 
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email", "phone_number", "isp_username", "customer_id")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "user_type")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (  # Fields when creating a user from admin
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "email", "phone_number", "isp_username", "customer_id", "user_type", "is_active"),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Check if the is_active field is being changed
        if change:
            old_obj = CustomUser.objects.get(pk=obj.pk)
            if not old_obj.is_active and obj.is_active:
                # Send activation email
                email_subject = "Your Account Has Been Activated!"
                email_body = render_to_string('activation_success_email.html', {'user': obj})

                email = EmailMultiAlternatives(email_subject, '', settings.EMAIL_HOST_USER, [obj.email])
                email.attach_alternative(email_body, 'text/html')
                email.send()

        # Save the model
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)