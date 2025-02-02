from django.contrib import admin
from .models import Bill, PaymentHistory, CollectionHistory

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'month', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'month')
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bill', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('user__username', 'bill__month')
    readonly_fields = ('payment_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        # Automatically set the user to the currently logged-in user
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(CollectionHistory)
class CollectionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'user', 'bill', 'amount', 'collection_date')
    list_filter = ('collection_date',)
    search_fields = ('staff__username', 'user__username', 'bill__month')
    readonly_fields = ('collection_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(staff=request.user)

    def save_model(self, request, obj, form, change):
        # Automatically set the staff to the currently logged-in user
        if not obj.staff:
            obj.staff = request.user
        super().save_model(request, obj, form, change)