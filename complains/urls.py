from django.urls import path
from .views import (
    ComplainListCreateView, ComplainDetailView,
    ReplyCreateView, CategoryListCreateView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('', ComplainListCreateView.as_view(), name='complain-list'),
    path('<int:pk>/', ComplainDetailView.as_view(), name='complain-detail'),
    path('<int:complain_id>/reply/', ReplyCreateView.as_view(), name='reply-create'),
]
