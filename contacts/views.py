from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination # ✅ 1. Puthiya Import
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags

from .models import Message
from .serializers import MessageSerializer

# ==========================================
# ✅ 2. Custom Pagination Class
# ==========================================
class MessagePagination(PageNumberPagination):
    page_size = 20  # Oru page-il ethra messages venam ennu ivide theerumanikkam
    page_size_query_param = 'page_size'
    max_page_size = 500

# ==========================================
# VIEWS
# ==========================================

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

# 2. Admin Dashboard - List all messages
class AdminMessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination # ✅ 3. Pagination ivide connect cheythu!

# 3. Admin Dashboard - View/Delete a single message
class AdminMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # ✅ 'CLICK' LOGIC: Message open aakumbol read status update aakum
    def get_object(self):
        obj = super().get_object()
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj

# 4. Admin Dashboard - Reply via Email & Update DB
class ReplyMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        
        # ✅ Already reply ayachittundengil block cheyyum!
        if message.is_replied:
            return Response(
                {"error": "This message has already been replied to."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        reply_text = request.data.get('reply_text')

        if not reply_text:
            return Response({"error": "Reply text is required"}, status=status.HTTP_400_BAD_REQUEST)

        subject = message.subject or 'Enquiry at ViceVersa'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [message.email]
        
        # --- SIMPLE PLAIN TEXT EMAIL ---
        text_content = f"Hi {message.name},\n\n{reply_text}\n\nBest Regards,\nTeam ViceVersa"

        try:
            send_mail(
                subject=subject, 
                message=text_content, 
                from_email=email_from, 
                recipient_list=recipient_list,
                fail_silently=False
            )
            
            message.reply_message = reply_text
            message.replied_at = timezone.now() 
            message.is_replied = True
            message.is_read = True 
            message.save()
            
            return Response({"message": "Reply sent successfully!"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": "Failed to send email. Check SMTP settings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)