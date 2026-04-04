from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    ClientListCreateView, ClientDetailView
)

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Client URLs
    path('list-create/', ClientListCreateView.as_view(), name='client-list-create'),
    path('detail/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
]