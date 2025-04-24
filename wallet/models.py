from django.db import models
import uuid
from users.models import User
from playrooms.models import Customer

class CoinsWallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coins_wallet') 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    coins_balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        owner = self.user or self.customer
        return f"Wallet for {owner} - {self.coins_balance} coins"

class CoinsTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('earn', 'Earn'),
        ('spend', 'Spend'),
        ('refund', 'Refund'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    coins_amount = models.IntegerField(default=0)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type.title()} of {self.coins_amount} coins"
    

