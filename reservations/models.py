from django.db import models
import uuid
from decimal import Decimal
from django.conf import settings
from playrooms.models import Location

class BookingStatus(models.TextChoices):
    NA_CEKANJU = 'NA_CEKANJU', 'Na čekanju'
    PRIHVACEN = 'PRIHVACEN', 'Prihvacen'
    ODBIJEN = 'ODBIJEN', 'Odbijen'
    OTKAZAN = 'OTKAZAN', 'Otkazan'

class Bookings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    customer = models.ForeignKey('playrooms.Customer', on_delete=models.CASCADE)
    customer_services = models.ManyToManyField('services.CustomerServices')
    location = models.ForeignKey('playrooms.Location', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings_set')
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.NA_CEKANJU)
    child = models.ForeignKey('users.Children', on_delete=models.CASCADE, null=True, blank=True)
    children_count = models.IntegerField(null=True, blank=True)
    booking_date = models.DateTimeField(null=True, blank=True)
    booking_start_time = models.DateTimeField(null=True, blank=True)
    booking_end_time = models.DateTimeField(null=True, blank=True)
    booking_duration = models.IntegerField(null=True, blank=True)
    booking_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    booking_validation_date = models.DateTimeField(null=True, blank=True)
    booking_type = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.public_id:
            last = Bookings.objects.order_by('-created_at').first()
            next_number = 1
            if last and last.public_id:
                try:
                    last_number = int(last.public_id.replace('BKG', ''))
                    next_number = last_number + 1
                except:
                    pass
            self.public_id = f"BKG{next_number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.public_id} - {self.customer} - {self.location} - {self.booking_date} - {self.status}"

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='ratings')
    booking = models.OneToOneField("Bookings", on_delete=models.CASCADE, related_name="rating")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'location', 'booking')