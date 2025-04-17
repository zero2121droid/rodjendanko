
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from services.models import Customer
from wallet.models import CoinsWallet

@receiver(post_save, sender=User)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created and not CoinsWallet.objects.filter(user=instance).exists():
        CoinsWallet.objects.create(user=instance, coins_balance=0)

@receiver(post_save, sender=Customer)
def create_wallet_for_customer(sender, instance, created, **kwargs):
    if created and not CoinsWallet.objects.filter(customer=instance).exists():
        CoinsWallet.objects.create(customer=instance, coins_balance=0)