from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Client
from .serializers import CategorySerializer, ClientSerializer

# ==========================================
# 1. CATEGORY MANAGEMENT VIEWS
# ==========================================

# Puthiya category add cheyyanum, list kanikkanum
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Oru category edit allengil delete cheyyan
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# ==========================================
# 2. CLIENT MANAGEMENT & FILTERING VIEWS
# ==========================================

# Puthiya client-ne add cheyyanum, pinne filter cheythu list edukkanum
class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Aadyam ella clients-neyum edukkunnu
        queryset = Client.objects.all().order_by('-created_at')
        
        # Frontend-il ninnu varunna filter parameters edukkunnu
        status = self.request.query_params.get('status')
        location = self.request.query_params.get('location')
        category_id = self.request.query_params.get('category')
        has_called = self.request.query_params.get('has_called')

        # Filter logic (Ningal paranja features)
        if status:
            queryset = queryset.filter(status=status)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if has_called is not None: 
            # Frontend-il ninnu 'true' or 'false' string aayi varumbol
            has_called_bool = has_called.lower() == 'true'
            queryset = queryset.filter(has_called=has_called_bool)
            
        return queryset

# Call vilichu kazhinju Status update cheyyanum, Edit/Delete cheyyanum
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]