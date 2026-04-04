from django.db import models

# 1. Category Model (Jewellery, Hospital, IT etc.)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# 2. Client Model
class Client(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'), # Initial status before calling
        ('Interested', 'Interested'),
        ('Not Interested', 'Not Interested'),
        ('Busy', 'Busy / Call Later'),
        ('Follow Up Later', 'Follow Up Later'),
    ]

    # Basic Details
    owner_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='clients')

    has_called = models.BooleanField(default=False) # Call button amarthi 'Yes' kodukkumbol ithu True aakum
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    follow_up_datetime = models.DateTimeField(blank=True, null=True) # Follow up later anengil Date & Time save cheyyan

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.owner_name})"