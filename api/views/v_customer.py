from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from playrooms.models import Customer
from api.serializers.s_customer import CustomerSerializer
from rest_framework.permissions import AllowAny
from api.serializers.s_customer_registration import CustomerRegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ---------------------------------------------------------------------
# Customer ViewSet
# ---------------------------------------------------------------------

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CustomerSerializer  # koristimo novi serializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__email", "first_name", "last_name"]
    filterset_fields = ["user"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at