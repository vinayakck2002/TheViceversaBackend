import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'viceversa_backend.settings') # ninte settings path
django.setup()

from clients.models import Client # ninte app peru 'clients' anennu karuthunnu

# 10 divasam munpathe date edukkunnu
cutoff_date = timezone.now() - timedelta(days=10)

# 10 divasathinu munpu delete aakkiyavare permanently delete cheyyunnu
old_clients = Client.objects.filter(is_deleted=True, deleted_at__lte=cutoff_date)
count = old_clients.count()
old_clients.delete()

print(f"Automatically deleted {count} clients from the Bin.")