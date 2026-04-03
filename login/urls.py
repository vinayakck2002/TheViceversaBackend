from django.urls import path
from .views import StandardLoginView, GoogleLoginView, LogoutView, CookieTokenRefreshView

urlpatterns = [
    path('login/', StandardLoginView.as_view(), name='standard_login'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]