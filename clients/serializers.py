from rest_framework import serializers
from .models import Category, Client
from django.utils import timezone

# 1. Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# 2. Client Serializer
class ClientSerializer(serializers.ModelSerializer):
    # Category-yude peru koodi JSON-il kittan vendi (Optional but helpful)
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Client
        fields = [
            'id', 'owner_name', 'company_name', 'phone_number',
            'location', 'category', 'category_name', 'note',
            'has_called', 'status', 'remarks', 'follow_up_datetime',
            'is_deleted', 'deleted_at', # 👈 Ithu randum add cheyyuka
            'created_at', 'updated_at'
        ]
    def get_days_left(self, obj):
        if obj.is_deleted and obj.deleted_at:
            # Delete cheytha divasavum innathe divasavum thammil ulla vyathyasam edukkunnu
            days_passed = (timezone.now() - obj.deleted_at).days
            remaining_days = 10 - days_passed
            
            # Remaining days minus-lekku pokathirikkan (0 aakki vekkan)
            return max(remaining_days, 0) 
        return None        