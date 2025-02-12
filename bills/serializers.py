from rest_framework import serializers
from .models import Bill, PaymentHistory, CollectionHistory
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, NotFound
from accounts.models import CustomUser

User = get_user_model()

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'user', 'month', 'amount', 'is_paid', 'created_at']
        read_only_fields = ['user', 'is_paid', 'created_at']

class PaymentHistorySerializer(serializers.ModelSerializer):
    bill = serializers.PrimaryKeyRelatedField(queryset=Bill.objects.filter(is_paid=False))  
    month = serializers.CharField(source='bill.month', read_only=True)  
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = PaymentHistory
        fields = ['id', 'user', 'bill', 'month', 'amount', 'payment_method', 'payment_date']
        read_only_fields = ['user', 'payment_method', 'payment_date', 'month']

    def validate_amount(self, value):
        if value < 100:
            raise ValidationError("Minimum payment amount is 100 TK.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user  
        bill = validated_data['bill'] 
        amount = validated_data['amount']
        
        if bill.is_paid:
            raise ValidationError("This bill has already been paid.")

        # Ensure the user is not overpaying
        if amount > bill.amount:
            raise ValidationError("Payment amount cannot exceed the bill amount.")
        

        # Check if the payment is less than the bill amount
        if amount < bill.amount:
            # Create a new bill for the remaining due amount
            due_amount = bill.amount - amount
            
            if due_amount < 100:
                raise ValidationError("Minimum due amount is 100 TK.")
            
            Bill.objects.create(user=user, month=bill.month, amount=due_amount)
        else:
            # Mark the bill as paid if full amount is covered
            bill.is_paid = True
            bill.save()

        # Create the payment history
        payment = PaymentHistory.objects.create(
            user=user,
            bill=bill,
            amount=amount,
            payment_method='online',  
        )

        return payment

    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'location']  

class CollectionHistorySerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(write_only=True)
    month = serializers.CharField(write_only=True)  
    display_month = serializers.SerializerMethodField()  
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = CollectionHistory
        fields = ['id', 'staff', 'user', 'bill', 'month', 'display_month', 'amount', 'collection_date', 'customer_id']
        read_only_fields = ['staff', 'user', 'bill', 'collection_date', 'display_month']

    def get_display_month(self, obj):
        """Retrieve month from the related Bill model for output"""
        return obj.bill.month if obj.bill else None

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        month = validated_data.pop('month')  

        try:
            user = CustomUser.objects.get(customer_id=customer_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this customer ID does not exist.")

        if PaymentHistory.objects.filter(user=user, bill__month=month).exists():
            raise serializers.ValidationError("Payment for this user and month already exists.")

        bill, created = Bill.objects.get_or_create(
            user=user,
            month=month,
            defaults={'amount': validated_data.get('amount', 0)}
        )

        validated_data['user'] = user
        validated_data['bill'] = bill

        return super().create(validated_data)

    def validate(self, data):
        customer_id = data.get('customer_id')
        month = data.get('month')

        try:
            user = CustomUser.objects.get(customer_id=customer_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this customer ID does not exist.")

        if PaymentHistory.objects.filter(user=user, bill__month=month).exists():
            raise serializers.ValidationError("Payment for this user and month already exists.")

        data['user'] = user
        return data
