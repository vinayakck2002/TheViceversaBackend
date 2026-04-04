from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination # ✅ 1. Puthiya Import
from .models import Category, Client
from .serializers import CategorySerializer, ClientSerializer

# ==========================================
# ✅ 2. Custom Pagination Class (15 items per page)
# ==========================================
class ClientPagination(PageNumberPagination):
    page_size = 15  # Oru page-il 15 clients varum
    page_size_query_param = 'page_size'
    max_page_size = 100

# ==========================================
# 1. CATEGORY MANAGEMENT VIEWS
# ==========================================

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# ==========================================
# 2. CLIENT MANAGEMENT & FILTERING VIEWS
# ==========================================

class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ClientPagination # ✅ 3. Pagination ivide connect cheythu!

    def get_queryset(self):
        queryset = Client.objects.all().order_by('-created_at')
        
        status = self.request.query_params.get('status')
        location = self.request.query_params.get('location')
        category_id = self.request.query_params.get('category')
        has_called = self.request.query_params.get('has_called')

        if status:
            queryset = queryset.filter(status=status)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if has_called is not None: 
            has_called_bool = has_called.lower() == 'true'
            queryset = queryset.filter(has_called=has_called_bool)
            
        return queryset

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]