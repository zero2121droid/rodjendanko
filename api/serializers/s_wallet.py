from rest_framework import serializers
from wallet.models import CoinsWallet, CoinsTransaction

# ---------------------------------------------------------------------
# Wallet Serializer
# ---------------------------------------------------------------------
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinsWallet
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
# ---------------------------------------------------------------------
# Wallet Transaction Serializer
# ---------------------------------------------------------------------
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinsTransaction
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

# ---------------------------------------------------------------------