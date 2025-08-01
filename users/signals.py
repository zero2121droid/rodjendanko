
import os
import shutil
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import User, Children
from playrooms.models import Customer
from wallet.models import CoinsWallet
from django.contrib.auth import get_user_model
from notifications.utils import create_notification
from django.contrib.auth.models import Group
# ---------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------
# Ovi signali se koriste za automatsko kreiranje novčanika i notifikacija
# prilikom registracije korisnika i kreiranja igraonice (Customer).
# Takođe, dodaju korisnika u grupu AdminGroup ako je admin.
# ---------------------------------------------------------------------

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

    # ➤ Ako je user_type admin, dodaj ga u grupu
    if instance.user_type == 'admin':
        admin_group, _ = Group.objects.get_or_create(name='AdminGroup')
        instance.groups.add(admin_group)
        logger.info(f"[User Group] Korisnik {instance.username} dodat u grupu AdminGroup")

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

# Briše folder slike deteta kada se obriše instanca Children modela
@receiver(post_delete, sender=Children)
def delete_child_image_folder(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        folder_path = os.path.dirname(image_path)

        # Obriši fajl ako postoji
        if os.path.isfile(image_path):
            os.remove(image_path)

        # Obriši ceo folder ako postoji
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)

