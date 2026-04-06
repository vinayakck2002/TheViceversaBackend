from django.urls import path
from .views import (
    HomeProjectListView, 
    ProjectListView, 
    AdminProjectListView, 
    ProjectCreateView, 
    ProjectDetailView
)

urlpatterns = [
    # ==========================
    # Public URLs (Website)
    # ==========================
    # 1. Home page projects (4 items) -> /api/projects/home/
    path('userlist/', HomeProjectListView.as_view(), name='project-home'),
    
    # 2. Main projects page (12 items) -> /api/projects/
    path('all/', ProjectListView.as_view(), name='project-list'),

    # ==========================
    # Admin URLs (Dashboard)
    # ==========================
    # 3. Admin list (20 items, includes drafts) -> /api/projects/admin/list/
    path('admin/list/', AdminProjectListView.as_view(), name='admin-project-list'),
    
    # 4. Admin create -> /api/projects/admin/create/
    path('admin/create/', ProjectCreateView.as_view(), name='project-create'),
    
    # 5. Admin edit/delete/detail -> /api/projects/admin/detail/<id>/
    path('admin/detail/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]