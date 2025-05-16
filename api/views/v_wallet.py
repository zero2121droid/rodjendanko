from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from wallet.models import CoinsWallet, CoinsTransaction
from api.serializers.s_wallet import WalletSerializer, WalletTransactionSerializer
from rest_framework.permissions import IsAuthenticated
# ---------------------------------------------------------------------
# Wallet ViewSet
# ---------------------------------------------------------------------
class WalletViewSet(viewsets.ModelViewSet):
    # queryset = CoinsWallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__email"]
    filterset_fields = ["user"] 
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="AdminGroup").exists() or user.is_superuser:
            return CoinsWallet.objects.all()
        return CoinsWallet.objects.filter(user=user)
# ---------------------------------------------------------------------
# Wallet Transaction ViewSet
# ---------------------------------------------------------------------
class WalletTransactionViewSet(viewsets.ModelViewSet):
    queryset = CoinsTransaction.objects.all()
    serializer_class = WalletTransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["transaction_type", "coins_amount", "user__email"]
    filterset_fields = ["transaction_type", "user"]  
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="AdminGroup").exists() or user.is_superuser:
            return CoinsTransaction.objects.all()
        return CoinsTransaction.objects.filter(user=user)
# ---------------------------------------------------------------------
# End of file
# ---------------------------------------------------------------------