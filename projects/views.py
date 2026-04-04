from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination # ✅ 1. Puthiya Import
from .models import Project
from .serializers import ProjectSerializer

# ==========================================
# ✅ 2. Custom Pagination Class (12 items per page)
# ==========================================
class ProjectPagination(PageNumberPagination):
    page_size = 12  # Oru page-il 12 projects varum
    page_size_query_param = 'page_size'
    max_page_size = 50

# ==========================================
# VIEWS
# ==========================================

# 1. Public Website-il Projects List Cheyyan (Aarkkum kanam)
class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    pagination_class = ProjectPagination # ✅ 3. Pagination ivide connect cheythu!

# 2. Admin Dashboard - Puthiya Project Add Cheyyan
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

# 3. Admin Dashboard - Project Edit/Delete Cheyyan
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]