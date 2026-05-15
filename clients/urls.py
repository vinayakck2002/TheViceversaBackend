from django.urls import path
from .views import *
urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('bin/', BinListView.as_view(), name='bin-list'),
    path('bin/<int:pk>/restore/', RestoreClientView.as_view(), name='bin-restore'),

    # Client URLs
    path('list-create/', ClientListCreateView.as_view(), name='client-list-create'),
    path('detail/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
]