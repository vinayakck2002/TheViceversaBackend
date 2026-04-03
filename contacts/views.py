from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags

from .models import Message
from .serializers import MessageSerializer

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny] # Aarkkum message ayakkam

# 2. Admin Dashboard - List all messages
class AdminMessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by('-created_at') # Puthiya messages aadyam varan
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated] # Admin mathram

# 3. Admin Dashboard - View/Delete a single message
class AdminMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # Message open cheyyumbol auto-read aakkan ulla puthiya function
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
        reply_text = request.data.get('reply_text')

        if not reply_text:
            return Response({"error": "Reply text is required"}, status=status.HTTP_400_BAD_REQUEST)

        subject = message.subject or 'Enquiry at ViceVersa'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [message.email]
        
        # --- KIDILAN HTML EMAIL TEMPLATE ---
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f7f6; padding: 20px; margin: 0;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    
                    <div style="background-color: #1a202c; padding: 20px; text-align: center;">
                        <h2 style="color: #ffffff; margin: 0; letter-spacing: 1px;">VICEVERSA</h2>
                    </div>
                    
                    <div style="padding: 30px; color: #333333; line-height: 1.6; font-size: 15px;">
                        <p>Hi <strong>{message.name}</strong>,</p>
                        <p style="white-space: pre-wrap;">{reply_text}</p>
                        
                        <hr style="border: none; border-top: 1px solid #eeeeee; margin: 30px 0;">
                        
                        <p style="margin: 0; color: #666666; font-size: 14px;">Best Regards,</p>
                        <p style="margin: 5px 0 0 0; font-weight: bold; color: #1a202c; font-size: 16px;">Team ViceVersa</p>
                    </div>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; text-align: center; color: #999999; font-size: 12px;">
                        <p style="margin: 0;">&copy; {timezone.now().year} ViceVersa. All rights reserved.</p>
                        <p style="margin: 5px 0 0 0;">Please do not reply directly to this automated email system.</p>
                    </div>
                    
                </div>
            </body>
        </html>
        """
        
        # HTML support illatha email client-ukalude (fallback) plain text
        text_content = strip_tags(html_content) 

        try:
            # Email ayakkunnu (Ivide html_message add cheythu)
            send_mail(
                subject=subject, 
                message=text_content, 
                from_email=email_from, 
                recipient_list=recipient_list,
                html_message=html_content # The Magic Happens Here!
            )
            
            # Database update cheyyunnu
            message.reply_message = reply_text
            message.replied_at = timezone.now() 
            message.is_replied = True
            message.is_read = True 
            message.save()
            
            return Response({"message": "Professional Email sent successfully!"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e) 
            return Response({"error": "Failed to send email. Check SMTP settings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)