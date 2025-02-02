from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Bill, PaymentHistory, CollectionHistory
from .serializers import BillSerializer, PaymentHistorySerializer, CollectionHistorySerializer
from .permissions import IsStaffUser
from rest_framework.exceptions import NotFound, ValidationError

class BillListView(generics.ListAPIView):
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user, is_paid=False)

class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return all payment history
        return PaymentHistory.objects.all()

    def perform_create(self, serializer):
        bill_id = self.request.data.get('bill')
        bill = Bill.objects.get(id=bill_id)
        serializer.save(user=self.request.user, bill=bill, payment_method='online')
        bill.is_paid = True
        bill.save()

class CollectionCreateView(generics.CreateAPIView):
    serializer_class = CollectionHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def perform_create(self, serializer):
        customer_id = self.request.data.get('customer_id')
        month = self.request.data.get('month')
        amount = self.request.data.get('amount')

        # Fetch the user based on customer_id
        user = serializer.validated_data['user']

        # Create or fetch the bill for the user and month
        bill, created = Bill.objects.get_or_create(
            user=user,
            month=month,
            defaults={'amount': amount}
        )

        # Save the collection history
        collection = serializer.save(staff=self.request.user, user=user, bill=bill)

        # Update the bill as paid
        bill.is_paid = True
        bill.save()

        # Create payment history for the user
        PaymentHistory.objects.create(
            user=user,
            bill=bill,
            amount=bill.amount,
            payment_method='offline',
        )

class PaymentHistoryListView(generics.ListAPIView):
    serializer_class = PaymentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentHistory.objects.filter(user=self.request.user)

class CollectionHistoryListView(generics.ListAPIView):
    serializer_class = CollectionHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        return CollectionHistory.objects.filter(staff=self.request.user)