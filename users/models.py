from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    public_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    USER_TYPES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('partner', 'Partner'),
        ('user', 'Regular User'),
    ]
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, null=True, blank=True)
    owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    terms_accepted = models.BooleanField(default=False)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    terms_accepted_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} ({self.email})"
    
    
    def save(self, *args, **kwargs):
        if not self.public_id:
            last = User.objects.order_by('-created_at').first()
            next_number = 1
            if last and last.public_id:
                try:
                    last_number = int(last.public_id.replace('USR', ''))
                    next_number = last_number + 1
                except:
                    pass
            self.public_id = f"USR{next_number:03d}"
        super().save(*args, **kwargs)

class Children(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.birth_date})" if self.name else "Unnamed child"
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)





