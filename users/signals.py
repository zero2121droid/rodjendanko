
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from playrooms.models import Customer
from wallet.models import CoinsWallet
from django.contrib.auth import get_user_model
from notifications.utils import create_notification
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(post_save, sender=User)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created and not CoinsWallet.objects.filter(user=instance).exists():
        CoinsWallet.objects.create(user=instance, coins_balance=100)
        logger.info(f"[User Wallet] Kreiran wallet za korisnika {instance.username} (ID: {instance.id})")
    create_notification(
            recipient=instance,
            title="Dobrodošli!",
            message="Uspešno ste se registrovali na Rodjendarijum.",
        )
    logger.info(f"[User Notif] Poslata notifikacija dobrodošlice korisniku {instance.username}")

@receiver(post_save, sender=Customer)
def create_notification_for_customer(sender, instance, created, **kwargs):
    if created:
        # Kreiraj notifikaciju za igraonicu (Customer)
        create_notification(
            recipient=instance.user,  # Ovo šalje notifikaciju vlasniku igraonice
            title="Dobrodošli!",
            message="Uspešno ste se registrovali na Rodjendarijum kao vlasnik igraonice.",
        )
        logger.info(f"[Customer Notif] Poslata notifikacija dobrodošlice korisniku {instance.name}")

