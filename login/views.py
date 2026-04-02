from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings # Settings import cheyyanam
from django.contrib.auth import authenticate

class GoogleLoginView(APIView):
    def post(self, request):
        # Frontend-il ninnu varunna token edukkunnu
        token = request.data.get('token')
        
        if not token:
            return Response({"error": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # .env file-il ninnu settings vazhi edukkunna Client ID vechu token verify cheyyunnu
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
            
            # Token-il ninnu user details edukkunnu
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            
            # User database-il illengil create cheyyunnu, undengil edukkunnu
            user, created = User.objects.get_or_create(username=email, defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
            
            # JWT Tokens Generate cheyyunnu
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Response Data set cheyyunnu
            response_data = {
                "message": "Login Successful",
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "name": f"{first_name} {last_name}".strip()
                }
            }
            
            response = Response(response_data, status=status.HTTP_200_OK)
            
            # Setting HttpOnly Cookies (Frontend Developer paranja pole Secure aayi vekkan)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,      # JavaScript-nu access cheyyan pattilla (Very Secure)
                secure=False,       # Localhost-il False aayirikkanam. Live (Vercel/Koyeb) aakumbol True aakkanam
                samesite='Lax',
                max_age=3600        # 1 hour validity
            )
            
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=86400 * 7   # 7 days validity
            )
            
            return response
            
        except ValueError:
            # Token invalid aanengil allengil expire aayengil
            return Response({"error": "Invalid Google Token"}, status=status.HTTP_400_BAD_REQUEST)
        

        

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if not email or not password:
            return Response({"error": "Email and Password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Email already undonnu check cheyyunnu (username aayi nammal email thanne aanu vekkunnathu)
        if User.objects.filter(username=email).exists():
            return Response({"error": "Email already registered. Please login."}, status=status.HTTP_400_BAD_REQUEST)

        # Puthiya user-e create cheyyunnu
        user = User.objects.create_user(
            username=email, # Username aayi email thanne set cheyyunnu
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return Response({"message": "Registration Successful"}, status=status.HTTP_201_CREATED)


class StandardLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # User-e verify cheyyunnu
        user = authenticate(username=email, password=password)

        if user is not None:
            # Login success aanengil Google auth-il cheytha pole JWT tokens generate cheyyunnu
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                "message": "Login Successful",
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "name": f"{user.first_name} {user.last_name}".strip()
                }
            }

            response = Response(response_data, status=status.HTTP_200_OK)

            # Same Cookie logic here
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False, # Live aakumbol True aakkanam
                samesite='Lax',
                max_age=3600
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=86400 * 7
            )

            return response
        else:
            return Response({"error": "Invalid Email or Password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        # Logout cheyyumbol Cookies delete cheyyunnu
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response