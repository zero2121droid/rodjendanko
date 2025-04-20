from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from wallet.models import CoinsWallet, CoinsTransaction
from api.serializers.s_wallet import WalletSerializer, WalletTransactionSerializer
# ---------------------------------------------------------------------
# Wallet ViewSet
# ---------------------------------------------------------------------
class WalletViewSet(viewsets.ModelViewSet):
    queryset = CoinsWallet.objects.all()
    serializer_class = WalletSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["customer"]
    filterset_fields = ["customer"] 
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  
# ---------------------------------------------------------------------
# Wallet Transaction ViewSet
# ---------------------------------------------------------------------
class WalletTransactionViewSet(viewsets.ModelViewSet):
    queryset = CoinsTransaction.objects.all()
    serializer_class = WalletTransactionSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["transaction_type", "amount", "customer"]
    filterset_fields = ["transaction_type"]  
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  
# ---------------------------------------------------------------------
# End of file
# ---------------------------------------------------------------------