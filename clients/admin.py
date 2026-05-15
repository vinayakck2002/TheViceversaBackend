from django.contrib import admin

# Register your models here.
from .models import Category, Client

admin.site.register(Category)
admin.site.register(Client)
