from django.urls import path
from .views import (
    AnnouncementListCreateView, AnnouncementDetailView,
    CommentListCreateView, CommentDetailView,
    ReactionCreateView, ReactionListView
)

urlpatterns = [
    # Announcement URLs
    path('', AnnouncementListCreateView.as_view(), name='announcement-list-create'),  # List and create announcements
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),  # Retrieve, update, delete a specific announcement

    # Comment URLs
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),  # List and create comments
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),  # Retrieve, update, delete a specific comment

    # Reaction URLs
    path('<int:announcement_id>/reactions/', ReactionCreateView.as_view(), name='reaction-create'),  # Add or update a reaction
    path('<int:announcement_id>/reactions/list/', ReactionListView.as_view(), name='reaction-list'),  # List reactions for an announcement
]