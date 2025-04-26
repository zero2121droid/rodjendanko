from django.db import models
import uuid


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='customer_profile')
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    customer_url = models.CharField(max_length=255, null=True, blank=True)
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    owner_lastname = models.CharField(max_length=255, null=True, blank=True)
    owner_email = models.EmailField(unique=True, null=True, blank=True)
    owner_password = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.public_id:
            last = Customer.objects.order_by('-created_at').first()
            next_number = 1
            if last and last.public_id:
                try:
                    last_number = int(last.public_id.replace('PRT', ''))
                    next_number = last_number + 1
                except:
                    pass
            self.public_id = f"PRT{next_number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    location_name = models.CharField(max_length=255)
    location_address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_name
    
    def save(self, *args, **kwargs):
        if not self.public_id:
            last = Location.objects.order_by('-created_at').first()
            next_number = 1
            if last and last.public_id:
                try:
                    last_number = int(last.public_id.replace('LOC', ''))
                    next_number = last_number + 1
                except:
                    pass
            self.public_id = f"LOC{next_number:03d}"
        super().save(*args, **kwargs)
    
    class Meta: # korisno za prilagodjavanje modela, omogucava postavljanje ljudskih imena za modele, redosled sortiranja, indeksa i drugih opcija
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['location_name'] # sortira po location_name

class LocationImages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    location_image_url = models.TextField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Image for {self.location.location_name}"

class LocationWorkingHours(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(null=True, blank=True)
    location_opening_time = models.TimeField(null=True, blank=True)
    location_closing_time = models.TimeField(null=True, blank=True)
    location_brake_duration = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Working hours for {self.location.location_name} on day {self.day_of_week}"

