from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from wallet.models import CoinsWallet, CoinsTransaction
from api.serializers.s_wallet import WalletSerializer, WalletTransactionSerializer
# ---------------------------------------------------------------------
# Wallet ViewSet
# ---------------------------------------------------------------------
class WalletViewSet(viewsets.ModelViewSet):
    # queryset = CoinsWallet.objects.all()
    serializer_class = WalletSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["customer__name", "user__email"]
    filterset_fields = ["customer", "user"] 
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return CoinsWallet.objects.all()
        if hasattr(user, "customer"):
            return CoinsWallet.objects.filter(customer=user.customer)
        return CoinsWallet.objects.filter(user=user)
# ---------------------------------------------------------------------
# Wallet Transaction ViewSet
# ---------------------------------------------------------------------
class WalletTransactionViewSet(viewsets.ModelViewSet):
    queryset = CoinsTransaction.objects.all()
    serializer_class = WalletTransactionSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["transaction_type", "amount", "customer__name", "user__email"]
    filterset_fields = ["transaction_type", "customer", "user"]  
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CoinsTransaction.objects.all()
        if hasattr(user, "customer"):
            return CoinsWallet.objects.filter(customer=user.customer)
        return CoinsWallet.objects.filter(user=user)
# ---------------------------------------------------------------------
# End of file
# ---------------------------------------------------------------------