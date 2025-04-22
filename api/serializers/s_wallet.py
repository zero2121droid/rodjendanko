from rest_framework import serializers
from wallet.models import CoinsWallet, CoinsTransaction

# ---------------------------------------------------------------------
# Wallet Serializer
# ---------------------------------------------------------------------
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinsWallet
        fields = '__all__'

    def validate(self, data):
        if data.get("customer") and data.get("user"):
            raise serializers.ValidationError("Wallet can be assigned to either a customer or a user, not both.")
        if not data.get("customer") and not data.get("user"):
            raise serializers.ValidationError("Wallet must be assigned to either a customer or a user.")
        return data

# ---------------------------------------------------------------------
# Wallet Transaction Serializer
# ---------------------------------------------------------------------
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinsTransaction
        fields = '__all__'

    def validate(self, data):
        if data.get("customer") and data.get("user"):
            raise serializers.ValidationError("Wallet can be assigned to either a customer or a user, not both.")
        if not data.get("customer") and not data.get("user"):
            raise serializers.ValidationError("Wallet must be assigned to either a customer or a user.")
        return data

# ---------------------------------------------------------------------