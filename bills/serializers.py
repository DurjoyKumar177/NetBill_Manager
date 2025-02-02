from rest_framework import serializers
from .models import Bill, PaymentHistory, CollectionHistory
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, NotFound

User = get_user_model()

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'user', 'month', 'amount', 'is_paid', 'created_at']
        read_only_fields = ['user', 'is_paid', 'created_at']

class PaymentHistorySerializer(serializers.ModelSerializer):
    bill = serializers.PrimaryKeyRelatedField(queryset=Bill.objects.filter(is_paid=False))  # Only unpaid bills
    month = serializers.CharField(source='bill.month', read_only=True)  # Auto-filled from bill
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
        user = self.context['request'].user  # Get logged-in user
        bill = validated_data['bill']  # Selected unpaid bill
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
            payment_method='online',  # Always set to 'online'
        )

        return payment

    
class CollectionHistorySerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(write_only=True)  # Add customer_id field
    month = serializers.CharField(write_only=True)  # Add month field

    class Meta:
        model = CollectionHistory
        fields = ['id', 'staff', 'user', 'bill','month', 'amount', 'collection_date', 'customer_id']
        read_only_fields = ['staff', 'user', 'bill', 'collection_date']

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')  # Remove from validated_data
        month = validated_data.pop('month')  # Remove from validated_data

        # Fetch the user based on customer_id
        try:
            user = User.objects.get(customer_id=customer_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this customer ID does not exist.")

        # Check if the user has already paid for this month
        if PaymentHistory.objects.filter(user=user, bill__month=month).exists():
            raise serializers.ValidationError("Payment for this user and month already exists.")

        # Get or create the bill
        bill, created = Bill.objects.get_or_create(
            user=user,
            month=month,
            defaults={'amount': validated_data.get('amount', 0)}
        )

        # Add user and bill to validated_data
        validated_data['user'] = user
        validated_data['bill'] = bill

        return super().create(validated_data)  # Create CollectionHistory

    customer_id = serializers.CharField(write_only=True)  # Add customer_id field
    month = serializers.CharField(write_only=True)  # Add month field

    class Meta:
        model = CollectionHistory
        fields = ['id', 'staff', 'user', 'bill', 'amount', 'collection_date', 'customer_id', 'month']
        read_only_fields = ['staff', 'user', 'bill', 'collection_date']

    def validate(self, data):
        customer_id = data.get('customer_id')
        month = data.get('month')

        # Fetch the user based on customer_id
        try:
            user = User.objects.get(customer_id=customer_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this customer ID does not exist.")

        # Check if the user has already paid for this month
        if PaymentHistory.objects.filter(user=user, bill__month=month).exists():
            raise serializers.ValidationError("Payment for this user and month already exists.")

        # Add user to the validated data
        data['user'] = user
        return data