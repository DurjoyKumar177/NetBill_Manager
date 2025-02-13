from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Bill, PaymentHistory, CollectionHistory
from .serializers import BillSerializer, PaymentHistorySerializer, CollectionHistorySerializer
from .permissions import IsStaffUser
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
import uuid
# from sslcommerz_python.payment import SSLCSession
from sslcommerz_lib import SSLCOMMERZ
from rest_framework import generics, permissions

class BillListView(generics.ListAPIView):
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user, is_paid=False)

class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PaymentHistory.objects.all()

    def create(self, request, *args, **kwargs):
        # Validate and process the request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bill_id = request.data.get('bill')
        bill = Bill.objects.get(id=bill_id)
        user = request.user

        if bill.is_paid:
            raise ValidationError("This bill has already been paid.")

        # Generate a unique transaction ID
        transaction_id = str(uuid.uuid4())

        # Initialize SSLCOMMERZ
        sslcz_settings = {
            'store_id': settings.SSL_COMMERZ_STORE_ID,
            'store_pass': settings.SSL_COMMERZ_STORE_PASSWORD,
            'issandbox': settings.SSL_COMMERZ_IS_TEST_MODE
        }
        sslcz = SSLCOMMERZ(sslcz_settings)

        # Prepare payment data
        post_body = {
            'total_amount': float(bill.amount),
            'currency': "BDT",
            'tran_id': transaction_id,
            'success_url': f"{settings.SITE_URL}{reverse('payment-success')}",
            'fail_url': f"{settings.SITE_URL}{reverse('payment-fail')}",
            'cancel_url': f"{settings.SITE_URL}{reverse('payment-cancel')}",
            'emi_option': 0,
            'cus_name': user.get_full_name() or "Unknown",
            'cus_email': user.email or "test@example.com",
            'cus_phone': getattr(user, 'phone_number', "01700000000"),
            'cus_add1': "N/A",
            'cus_city': "N/A",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': "Internet Bill Payment",
            'product_category': "Utility Bill",
            'product_profile': "general",
            'value_a': str(bill.id)  
        }

        # Create SSLCOMMERZ session
        response = sslcz.createSession(post_body)
        print("SSLCOMMERZ response:", response)

        if "GatewayPageURL" in response:
            # Return the payment gateway URL to the frontend
            return Response(
                {
                    "payment_url": response["GatewayPageURL"],
                    "transaction_id": transaction_id
                },
                status=status.HTTP_200_OK
            )
        else:
            raise ValidationError("Failed to initiate payment with SSLCOMMERZ.")


class SSLCOMMERZSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        return self.process_payment(request)

    def post(self, request, *args, **kwargs):
        return self.process_payment(request)

    def process_payment(self, request):
        bill_id = request.GET.get("value_a") or request.POST.get("value_a")

        # Debugging print statement
        print(f"Received bill_id: {bill_id}")  

        # Check if bill_id is valid
        if not bill_id or not bill_id.isdigit():
            return Response({"error": "Invalid bill ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bill = Bill.objects.get(id=int(bill_id))

            # Create payment history for the user
            PaymentHistory.objects.create(
                user=bill.user,
                bill=bill,
                amount=bill.amount,
                payment_method='online',
            )

            # Mark bill as paid
            bill.is_paid = True
            bill.save()

            return Response(status=status.HTTP_302_FOUND, headers={"Location": f"{settings.FRONTEND_URL}/payment-success"})
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_400_BAD_REQUEST)



class SSLCOMMERZFailView(APIView):
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_302_FOUND, headers={"Location": f"{settings.FRONTEND_URL}/payment-failed"})

class SSLCOMMERZCancelView(APIView):
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_302_FOUND, headers={"Location": f"{settings.FRONTEND_URL}/payment-cancel"})

class SSLCOMMERZIPNView(APIView):
    def post(self, request, *args, **kwargs):
        transaction_id = request.POST.get("tran_id")
        status = request.POST.get("status")
        bill_id = request.POST.get("value_a")  # Custom field to track bill ID

        try:
            bill = Bill.objects.get(id=bill_id)

            if status == "VALID":
                # Create payment history for the user
                payment = PaymentHistory.objects.create(
                    user=bill.user,
                    bill=bill,
                    amount=bill.amount,
                    payment_method='online',
                    transaction_id=transaction_id
                )

                # Mark bill as paid
                bill.is_paid = True
                bill.save()

                return Response({"message": "Payment confirmed via IPN!"})
            else:
                return Response({"message": "Payment verification failed!"})
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_400_BAD_REQUEST)

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