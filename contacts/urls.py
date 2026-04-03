from django.urls import path
from .views import (
    ContactMessageCreateView, 
    AdminMessageListView, 
    AdminMessageDetailView, 
    ReplyMessageView
)

urlpatterns = [
    # Public URL
    path('create/', ContactMessageCreateView.as_view(), name='contact_message'),
    
    # Admin URLs
    path('admin/list/', AdminMessageListView.as_view(), name='admin_messages'),
    path('admin/Detail/<int:pk>/', AdminMessageDetailView.as_view(), name='admin_message_detail'),
    path('admin/<int:pk>/reply/', ReplyMessageView.as_view(), name='message_reply'),
]