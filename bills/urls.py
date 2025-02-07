from django.urls import path
from .views import (
    BillListView, PaymentCreateView, CollectionCreateView,
    PaymentHistoryListView, CollectionHistoryListView,
    SSLCOMMERZSuccessView, SSLCOMMERZFailView, SSLCOMMERZCancelView, SSLCOMMERZIPNView
)

urlpatterns = [
    path('', BillListView.as_view(), name='bill-list'),
    path('payments/', PaymentCreateView.as_view(), name='payment-create'),
    path('collections/', CollectionCreateView.as_view(), name='collection-create'),
    path('payment-history/', PaymentHistoryListView.as_view(), name='payment-history'),
    path('collection-history/', CollectionHistoryListView.as_view(), name='collection-history'),
    
    # SSLCOMMERZ Payment URLs
    path('payment/success/', SSLCOMMERZSuccessView.as_view(), name='payment-success'),
    path('payment/fail/', SSLCOMMERZFailView.as_view(), name='payment-fail'),
    path('payment/cancel/', SSLCOMMERZCancelView.as_view(), name='payment-cancel'),
    path('payment/ipn/', SSLCOMMERZIPNView.as_view(), name='payment-ipn'),
]