from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Aadyam Header-il token undengil athu edukkan nokkum
        header = self.get_header(request)
        
        if header is None:
            # Header-il illel, 'access_token' enna Cookie-yil ninnu edukkum
            raw_token = request.COOKIES.get('access_token')
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token