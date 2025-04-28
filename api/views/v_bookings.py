from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from reservations.models import Bookings
from api.serializers.s_bookings import BookingsSerializer
from notifications.utils import create_notification
from api.utils import add_swagger_tags

# ---------------------------------------------------------------------
# Bookings Permissions
# ---------------------------------------------------------------------
class IsBookingOwnerOrCustomerOrAdmin(permissions.BasePermission):
    """
    Dozvoljava pristup samo:
    - korisniku koji je kreirao rezervaciju,
    - vlasniku lokacije (Customer),
    - ili adminu (superuseru).
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        if obj.user == user:
            return True
        if hasattr(user, 'customer_profile') and obj.customer == user.customer_profile:
            return True
        return False

# ---------------------------------------------------------------------
# Bookings ViewSet
# ---------------------------------------------------------------------
@add_swagger_tags(tags=["Bookings"])
class BookingsViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrCustomerOrAdmin]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["customer__name", "location__location_name", "customer_services__service_name", "booking_date"]
    filterset_fields = ["customer", "location", "booking_date", "status"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Bookings.objects.all()
        if hasattr(user, 'customer_profile'):
            return Bookings.objects.filter(customer=user.customer_profile)
        return Bookings.objects.filter(user=user)

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        create_notification(
            recipient=self.request.user,
            title="Uspešna rezervacija",
            message=f"Vaša rezervacija za {booking.location.location_name} je uspešno kreirana.",
        )
# ---------------------------------------------------------------------