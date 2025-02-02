from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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

admin.site.register(CustomUser, CustomUserAdmin)
