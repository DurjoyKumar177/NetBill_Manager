from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import CustomUser
from .models import CustomUser, AdditionalUserInfo, UserPackageInfo, Device


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    profile_pic = serializers.ImageField(required=False)  # Allow optional profile picture

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'isp_username', 'customer_id', 'password', 'confirm_password', 'location', 'profile_pic']

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Ensure customer_id and isp_username are unique
        if CustomUser.objects.filter(isp_username=data.get('isp_username')).exists():
            raise serializers.ValidationError({"isp_username": "This ISP username is already in use."})
        if CustomUser.objects.filter(customer_id=data.get('customer_id')).exists():
            raise serializers.ValidationError({"customer_id": "This Customer ID is already registered."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        profile_pic = validated_data.pop('profile_pic', None)  # Handle optional profile picture separately

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            isp_username=validated_data['isp_username'],
            customer_id=validated_data['customer_id'],
            password=validated_data['password'],
            location=validated_data.get('location', ''),  # Handle optional location
            is_active=False  
        )

        if profile_pic:
            user.profile_pic = profile_pic
            user.save()

        # Send a registration confirmation email
        email_subject = "Registration Successful"
        email_body = render_to_string('register_success.html', {'user': user})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()

        return user

class AdditionalUserInfoSerializer(serializers.ModelSerializer):
    devices = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all(), many=True)  # Ensure devices field supports multiple selections

    class Meta:
        model = AdditionalUserInfo
        fields = ['local_area', 'road_number', 'building_name', 'room_no', 'router_model', 'devices']

    def update(self, instance, validated_data):
        devices_data = validated_data.pop('devices', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if devices_data is not None:
            instance.devices.set(devices_data)  # .set() for ManyToManyField

        return instance


class UserPackageInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPackageInfo
        fields = ['package_number', 'customer_id', 'isp_username', 'package_password', 'monthly_payment', 'package_slip']

class CustomUserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    additional_info = AdditionalUserInfoSerializer(required=False)
    package_info = UserPackageInfoSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'location', 'profile_pic', 'additional_info', 'package_info']

    def update(self, instance, validated_data):
        additional_info_data = validated_data.pop('additional_info', None)
        package_info_data = validated_data.pop('package_info', None)

        # Update CustomUser fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle AdditionalUserInfo
        if additional_info_data:
            devices_data = additional_info_data.pop('devices', None) 
            
            additional_info, created = AdditionalUserInfo.objects.update_or_create(
                user=instance, defaults=additional_info_data
            )
            
            if devices_data is not None:
                additional_info.devices.set(devices_data)  
            
            additional_info.save()

        # Handle UserPackageInfo
        if package_info_data:
            UserPackageInfo.objects.update_or_create(user=instance, defaults=package_info_data)

        return instance

    
