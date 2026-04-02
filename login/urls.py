from django.urls import path
from .views import GoogleLoginView, RegisterView, StandardLoginView, LogoutView

urlpatterns = [
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', StandardLoginView.as_view(), name='standard_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]