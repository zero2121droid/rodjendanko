from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from reservations.models import Bookings
from api.serializers.s_bookings import BookingsSerializer
from notifications.utils import create_notification
# ---------------------------------------------------------------------
# Bookings ViewSet
# ---------------------------------------------------------------------
class BookingsViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["customer", "location", "service", "booking_date"]
    filterset_fields = ["customer", "location", "booking_date", "status"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Bookings.objects.all()
        return Bookings.objects.filter(user=user)

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        # 👇 Slanje notifikacije nakon kreiranja rezervacije
        create_notification(
            recipient=self.request.user,
            title="Uspešna rezervacija",
            message=f"Vaša rezervacija za {booking.location.name} je uspešno kreirana.",
            #link=f"/moje-rezervacije/{booking.id}"
        )
# ---------------------------------------------------------------------