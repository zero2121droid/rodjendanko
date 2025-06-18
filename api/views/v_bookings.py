from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from reservations.models import Bookings
from api.serializers.s_bookings import BookingsSerializer
from notifications.utils import create_notification
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from reservations.filters import BookingFilter
from django.utils.timezone import now
from django.db.models import Func,F, ExpressionWrapper, DateTimeField
from django.db.models.functions import Cast

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
class BookingsViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrCustomerOrAdmin]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["customer__name", "location__location_name", "customer_services__service_name", "booking_date"]
    filterset_fields = ['customer', 'location', 'booking_date', 'status']
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="AdminGroup").exists() or user.is_superuser:
            return Bookings.objects.all().order_by("created_at")
        if hasattr(user, 'customer_profile'):
            return Bookings.objects.filter(customer=user.customer_profile).order_by("created_at")
        return Bookings.objects.filter(user=user).order_by("created_at")

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        create_notification(
            recipient=self.request.user,
            title="Uspešna rezervacija",
            message=f"Vaša rezervacija za {booking.location.location_name} je uspešno kreirana.",
        )
    
    def update(self, request, *args, **kwargs):
        booking = self.get_object()

    # Dodatna sigurnost: samo vlasnik ili admin može menjati vreme i datum
        user = request.user
        if not (
            user.is_superuser or
            (hasattr(user, 'customer_profile') and booking.customer == user.customer_profile)
        ):
        # Ako je običan korisnik, može menjati samo opis ili otkazati rezervaciju
            allowed_fields = {'description', 'status'}
            if not set(request.data.keys()).issubset(allowed_fields):
                return Response(
                    {"detail": "Nemate dozvolu da menjate ove informacije."},
                    status=403
                )
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='user-booking-count')
    def user_booking_count(self, request):
        user = request.user
        now = timezone.now()
        count = Bookings.objects.filter(user=user, booking_start_time__gte=now).count()
        return Response({'count': count})
    # ---------------------------------------------------------------------
    # Endpoint za preuzimanje svih aktivnih rezervacija
    # ---------------------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='active')
    def active_bookings(self, request):
        now_dt = timezone.now()

        active = self.get_queryset().filter(
            booking_end_time__gte=now_dt
        )

        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True) 
        return Response(serializer.data)