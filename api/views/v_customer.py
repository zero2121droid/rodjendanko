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
    serializer_class = CustomerSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "last_name", "email", "city", "phone"]
    filterset_fields = ["city"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({"message": "Igraonica uspešno registrovana!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)