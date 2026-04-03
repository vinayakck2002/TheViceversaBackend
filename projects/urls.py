from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDetailView

urlpatterns = [
    # Public URL
    path('list/', ProjectListView.as_view(), name='project-list'),
    
    # Admin URLs
    path('admin/create/', ProjectCreateView.as_view(), name='project-create'),
    path('admin/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]