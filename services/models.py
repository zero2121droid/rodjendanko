from django.db import models
import uuid
from playrooms.models import Customer
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ServiceType(models.TextChoices):
    PROSLAVA = 'Proslava Rodjendana'
    OSTALO = 'Ostalo'

class PaymentMethod(models.TextChoices):
    BESPLATNO = 'Besplatno'
    NAPLATA = 'Naplata'
    DRUGO = 'Drugo'

class CustomerServices(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=50, choices=ServiceType.choices)
    duration = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price_per_child = models.DecimalField(max_digits=5, decimal_places=2)
    min_quantity = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=0)
    other_services = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey('playrooms.Location', on_delete=models.CASCADE, null=True, blank=True)
    service_image_url = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices)
    coins_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_name} ({self.customer.name})"
    
    def clean(self):
        if self.price_per_child < 0:
            raise ValidationError("Cena usluge ne može biti negativna.")
    
class PartnerServices(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    delivery = models.BooleanField(default=False)
    product_image_url = models.TextField(null=True, blank=True)
    coins_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} ({self.partner.name})"
    def clean(self):
        if self.price_per_unit < 0:
            raise ValidationError("Cena usluge ne može biti negativna.")

class OtherServices(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.TextField()
    other_service_image_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    def clean(self):
        if self.price_per_unit < 0:
            raise ValidationError("Cena usluge ne može biti negativna.")

class ServicesImages (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    service_type = models.CharField(max_length=255)
    service_image_url = models.TextField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Slika za: {self.service_type} - {self.object_id}"
    def save(self, *args, **kwargs):
        if not self.service_type and self.content_type:
            self.service_type = self.content_type.model
        super().save(*args, **kwargs)



