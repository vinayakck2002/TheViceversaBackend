from rest_framework import generics, filters # ✅ filters import cheythu
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination # ✅ Pagination import cheythu
from .models import Category, Client
from .serializers import CategorySerializer, ClientSerializer

# ==========================================
# ✅ CUSTOM PAGINATION (20 items per page)
# ==========================================
class ClientPagination(PageNumberPagination):
    page_size = 20
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
    pagination_class = ClientPagination # ✅ Pagination connect cheythu

    # ✅ SEARCH SETUP
    filter_backends = [filters.SearchFilter]
    search_fields = ['owner_name', 'company_name', 'phone_number', 'location'] # Ee 4 fields vechu thedam

    def get_queryset(self):
        # Aadyam ella clients-neyum edukkunnu
        queryset = Client.objects.all().order_by('-created_at')
        
        # Frontend-il ninnu varunna filter parameters edukkunnu
        status = self.request.query_params.get('status')
        has_called = self.request.query_params.get('has_called')
        remarks = self.request.query_params.get('remarks')
        follow_up_date = self.request.query_params.get('follow_up_date') # Date aayi thedan

        # ✅ FILTER LOGIC
        if status:
            queryset = queryset.filter(status=status)
            
        if has_called is not None: 
            has_called_bool = has_called.lower() == 'true'
            queryset = queryset.filter(has_called=has_called_bool)
            
        if remarks:
            queryset = queryset.filter(remarks__icontains=remarks) # Remarks-il aa vakkundengil edukkum
            
        if follow_up_date:
            # Frontend ninnu 'YYYY-MM-DD' format-il varumbol athu vechu filter cheyyan
            queryset = queryset.filter(follow_up_datetime__date=follow_up_date)
            
        return queryset

# Call vilichu kazhinju Status update cheyyanum, Edit/Delete cheyyanum
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]