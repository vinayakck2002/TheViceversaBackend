from rest_framework import serializers
from .models import Category, Client

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
            'location', 'category', 'category_name', 
            'has_called', 'status', 'remarks', 'follow_up_datetime',
            'created_at'
        ]