from rest_framework import serializers
from wallet.models import CoinsWallet, CoinsTransaction

# ---------------------------------------------------------------------
# Wallet Serializer
# ---------------------------------------------------------------------
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinsWallet
        fields = '__all__'

# ---------------------------------------------------------------------
# Wallet Transaction Serializer
# ---------------------------------------------------------------------
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinsTransaction
        fields = '__all__'

# ---------------------------------------------------------------------