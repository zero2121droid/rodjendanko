from django.db import models
import uuid

class BookingStatus(models.TextChoices):
    NA_CEKANJU = 'Na čekanju'
    PRIHVACEN = 'Prihvacen'
    ODBIJEN = 'Odbijen'
    OTKAZAN = 'Otkazan'

class Bookings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('playrooms.Customer', on_delete=models.CASCADE)
    customer_services = models.ForeignKey('services.CustomerServices', on_delete=models.CASCADE)
    location = models.ForeignKey('playrooms.Location', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.NA_CEKANJU)
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_validation_date = models.DateTimeField(null=True, blank=True)
    booking_type = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} - {self.customer} - {self.location} - {self.booking_date} - {self.status}"
