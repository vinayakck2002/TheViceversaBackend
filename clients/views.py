from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError # ✅ Validation error kaanikkan
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
    pagination_class = ClientPagination

    # ✅ SEARCH SETUP
    filter_backends = [filters.SearchFilter]
    search_fields = ['owner_name', 'company_name', 'phone_number', 'location']

    def get_queryset(self):
        queryset = Client.objects.all().order_by('-created_at')
        
        status = self.request.query_params.get('status')
        has_called = self.request.query_params.get('has_called')
        remarks = self.request.query_params.get('remarks')
        follow_up_date = self.request.query_params.get('follow_up_date') 
        category_id = self.request.query_params.get('category')

        if status:
            queryset = queryset.filter(status=status)
            
        if has_called is not None: 
            has_called_bool = has_called.lower() == 'true'
            queryset = queryset.filter(has_called=has_called_bool)
            
        if remarks:
            queryset = queryset.filter(remarks__icontains=remarks)
            
        if follow_up_date:
            queryset = queryset.filter(follow_up_datetime__date=follow_up_date)
            
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset

    # ✅ DUPLICATE CHECK LOGIC (Number & Company Name)
    def perform_create(self, serializer):
        phone_number = self.request.data.get('phone_number')
        company_name = self.request.data.get('company_name')

        # Phone number check
        if Client.objects.filter(phone_number=phone_number).exists():
            raise ValidationError({"phone_number": "Already  this phone number exists in the database!"})

        # Company name check
        if Client.objects.filter(company_name=company_name).exists():
            raise ValidationError({"company_name": "Already  this company name exists in the database!"})

        serializer.save()

# Call vilichu kazhinju Status update cheyyanum, Edit/Delete cheyyanum
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]