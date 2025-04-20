from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from playrooms.models import Customer
from api.serializers.s_customer import CustomerSerializer

# ---------------------------------------------------------------------
# Customer ViewSet
# ---------------------------------------------------------------------

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "last_name", "email", "city", "phone"]
    filterset_fields = ["city"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at