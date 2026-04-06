from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Project
from .serializers import ProjectSerializer


# ==========================================
# ✅ 1. PAGINATION CLASSES (3 tharam)
# ==========================================
class HomeProjectPagination(PageNumberPagination):
    page_size = 4  # Home page-il 4 projects

class PublicProjectPagination(PageNumberPagination):
    page_size = 12  # Website projects page-il 12 projects

class AdminProjectPagination(PageNumberPagination):
    page_size = 20  # Admin dashboard-il 20 projects

# ==========================================
# ✅ 2. PUBLIC VIEWS (Website-nu vendi)
# ==========================================

# Home Page (Published AND show_on_home=True aaya 4 items mathram)
class HomeProjectListView(generics.ListAPIView):
    queryset = Project.objects.filter(is_published=True, show_on_home=True).order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    pagination_class = HomeProjectPagination 

# Projects Page (Published aaya 12 items mathram)
class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    pagination_class = PublicProjectPagination 

# ==========================================
# ✅ 3. ADMIN VIEWS (Dashboard-nu vendi)
# ==========================================

# Admin List (Ellam kanikkan - Drafts + Published)
class AdminProjectListView(generics.ListAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = AdminProjectPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

# Admin - Puthiya Project Add Cheyyan
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

# Admin - Project Edit/Delete Cheyyan
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]