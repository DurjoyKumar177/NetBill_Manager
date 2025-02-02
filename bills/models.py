from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bills')
    month = models.CharField(max_length=20)  # Format: "YYYY-MM"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for  - {self.month} - ({self.amount} TK)"

class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_history')
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payment_history')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('online', 'Online'), ('offline', 'Offline')])
    payment_date = models.DateTimeField(auto_now_add=True)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        return f"Payment by {self.user.username} - {self.bill.month}"

class CollectionHistory(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collection_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collected_payments')
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='collection_history')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    collection_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Collection by {self.staff.username} from {self.user.username} - {self.bill.month}"