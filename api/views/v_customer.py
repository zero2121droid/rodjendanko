from rest_framework import viewsets, filters, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from playrooms.models import Customer
from api.serializers.s_customer import CustomerSerializer
from rest_framework.permissions import AllowAny, SAFE_METHODS
from api.serializers.s_customer_registration import CustomerRegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


# ---------------------------------------------------------------------
# Pristup Customeru samo za Ownera
# ---------------------------------------------------------------------
class IsOwnerOfCustomer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Dozvoli read-only pristup svima koji su autentifikovani
        if request.method in SAFE_METHODS:
            return True
        # Za pisanje, dozvoli samo vlasniku ili superuseru
        return obj.user == request.user or request.user.is_superuser

# ---------------------------------------------------------------------
# Customer ViewSet
# ---------------------------------------------------------------------
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfCustomer]
    serializer_class = CustomerSerializer  # koristimo novi serializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__email", "name", "owner_name", "owner_lastname"]
    filterset_fields = ["user"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        return Customer.objects.all().order_by("created_at")