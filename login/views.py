from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({"error": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
            email = idinfo.get('email')

            # --- VIP SECURITY CHECK ---
            if email != settings.ALLOWED_ADMIN_EMAIL:
                return Response({"error": "Access Denied. Only Admin can login."}, status=status.HTTP_403_FORBIDDEN)
            # --------------------------
            
            # Username-um Email-um mathram vachu user-e edukkunnu / undakkunnu
            user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            
            refresh = RefreshToken.for_user(user)
            
            # Response Data - Email mathram!
            response_data = {
                "message": "Login Successful",
                "user": {
                    "email": user.email
                }
            }
            
            response = Response(response_data, status=status.HTTP_200_OK)
            
            # samesite='None' & secure=True is MUST for cross-origin cookies
            response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True, secure=True, samesite='None', max_age=3600)
            response.set_cookie(key='refresh_token', value=str(refresh), httponly=True, secure=True, samesite='None', max_age=86400 * 7)
            
            return response
            
        except ValueError:
            return Response({"error": "Invalid Google Token"}, status=status.HTTP_400_BAD_REQUEST)


class StandardLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email != settings.ALLOWED_ADMIN_EMAIL:
            return Response({"error": "Access Denied"}, status=403)

        user = authenticate(username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            response = Response({
                "message": "Login Successful",
                "user": {"email": user.email}
            })

            # ✅ Cookie FIX
            response.set_cookie(
                'access_token',
                str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='None',
                max_age=3600
            )

            response.set_cookie(
                'refresh_token',
                str(refresh),
                httponly=True,
                secure=True,
                samesite='None',
                max_age=86400 * 7
            )

            return response

        return Response({"error": "Invalid Email or Password"}, status=401)

class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"error": "No refresh token"}, status=401)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            response = Response({"message": "Refreshed"})

            # ✅ Cookie FIX
            response.set_cookie(
                'access_token',
                new_access_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=3600
            )

            return response

        except TokenError:
            return Response({"error": "Invalid refresh"}, status=401)


class LogoutView(APIView):

    def post(self, request):
        response = Response({"message": "Logged out"})

        # ✅ Cookie FIX
        response.delete_cookie('access_token', samesite='None')
        response.delete_cookie('refresh_token', samesite='None')

        return response