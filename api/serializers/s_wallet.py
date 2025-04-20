from rest_framework import serializers
from wallet.models import Wallet, WalletTransaction

# ---------------------------------------------------------------------
# Wallet Serializer
# ---------------------------------------------------------------------
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

# ---------------------------------------------------------------------
# Wallet Transaction Serializer
# ---------------------------------------------------------------------
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'

# ---------------------------------------------------------------------