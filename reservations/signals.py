
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bookings, BookingStatus
from notifications.utils import create_notification

@receiver(post_save, sender=Bookings)
def send_booking_confirmation_notification(sender, instance, created, **kwargs):
    if not created and instance.status == BookingStatus.PRIHVACEN:
        create_notification(
            user=instance.user,
            title="Rezervacija potvrđena",
            message=f"Vaša rezervacija za {instance.location.location_name} je potvrđena!",
            #link=f"/moje-rezervacije/{instance.id}"
        )
