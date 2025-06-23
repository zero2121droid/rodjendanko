
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Bookings, BookingStatus
from notifications.utils import create_notification
from django.utils import timezone
from datetime import datetime

@receiver(post_save, sender=Bookings)
def send_booking_confirmation_notification(sender, instance, created, **kwargs):
   if not created:
        link = f"/moje-rezervacije/{instance.id}"
        if instance.status == BookingStatus.PRIHVACEN:
            create_notification(
                recipient=instance.user,
                title="Rezervacija potvrđena",
                message=f"Vaša rezervacija za {instance.location.location_name} je potvrđena!",
                link=link
            )
        elif instance.status == BookingStatus.ODBIJEN:
            create_notification(
                recipient=instance.user,
                title="Rezervacija odbijena",
                message=f"Nažalost, vaša rezervacija za {instance.location.location_name} je odbijena.",
                link=link
            )

@receiver(pre_save, sender=Bookings)
def set_validation_date_on_status_change(sender, instance, **kwargs):
    if instance.booking_start_time:
        instance.booking_date = instance.booking_start_time.replace(
            hour=0, minute=0, second=0, microsecond=0
    )
    # Proveri da li objekat već postoji u bazi (tj. da li je to nova instanca)
    if instance.pk:
        try:
            previous = Bookings.objects.get(pk=instance.pk)
            # Provera da li je status promenjen
            if previous.status != instance.status:
                if instance.status in [BookingStatus.PRIHVACEN, BookingStatus.ODBIJEN]:
                    instance.booking_validation_date = timezone.now()
        except Bookings.DoesNotExist:
            # Ako objekat ne postoji, znači da je ovo nova rezervacija, pa ništa ne treba da se menja
            pass
