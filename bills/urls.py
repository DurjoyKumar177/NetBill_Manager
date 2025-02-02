from django.urls import path
from .views import (
    BillListView, PaymentCreateView, CollectionCreateView,
    PaymentHistoryListView, CollectionHistoryListView
)

urlpatterns = [
    path('', BillListView.as_view(), name='bill-list'),
    path('payments/', PaymentCreateView.as_view(), name='payment-create'),
    path('collections/', CollectionCreateView.as_view(), name='collection-create'),
    path('payment-history/', PaymentHistoryListView.as_view(), name='payment-history'),
    path('collection-history/', CollectionHistoryListView.as_view(), name='collection-history'),
]