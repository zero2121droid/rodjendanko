from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
import shutil
from django.conf import settings

class User(AbstractUser):
    public_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    USER_TYPES = [
        ('admin', 'Admin'),
        #('customer', 'Customer'),
        ('partner', 'Partner'),
        ('user', 'Regular User'),
    ]
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
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
    
    # Funkcija za kreiranje jedinstvenog public_id za korisnika. Koristi se prilikom kreiranja novog korisnika. Mora da bude smestena u modelu User jer se koristi prilikom kreiranja svakog korisnika, Kada bi se definisala u serializeru onda bi se 
    # pozivala samo prilikom pozivanja tog serializera tj endpointa, a potrebno je da se poziva prilikom kreiranja svakog korisnika
    def save(self, *args, **kwargs):
        if not self.public_id:
            last = User.objects.exclude(public_id__isnull=True).exclude(public_id='').order_by('-created_at').first()
            next_number = 1
            if last and last.public_id:
                try:
                    last_number = int(last.public_id.replace('USR', ''))
                    next_number = last_number + 1
                except:
                    pass
            self.public_id = f"USR{next_number:03d}"
        super().save(*args, **kwargs)

# Function to generate a unique upload path for child images

def child_image_upload_path(instance, filename):
    return f'users/{instance.user.id}/children/{instance.id}/{filename}'

class Children(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=child_image_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.birth_date})" if self.name else "Unnamed child"
    
    def save(self, *args, **kwargs):
        try:
            # Uzimamo instancu iz baze pre nego što se izvrši update
            old_instance = Children.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                # Ako je stara slika različita od nove -> brišemo staru
                old_instance.image.delete(save=False)
        except Children.DoesNotExist:
            pass  # Novi objekat, nema prethodne slike

        super().save(*args, **kwargs)
    
    @property
    def years(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

@receiver(post_delete, sender=Children)
def delete_child_folder_on_delete(sender, instance, **kwargs):
    folder_path = os.path.join(settings.MEDIA_ROOT, 'children', str(instance.id))

    # Briši celu fasciklu ako postoji
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)




