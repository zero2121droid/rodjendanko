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
from reservations.models import BookingStatus
from django.utils.timezone import make_aware
from django.db.models import Q

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
        if user.groups.filter(name="AdminGroup").exists():
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
    lookup_field = 'public_id'
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
        user = request.user
        is_admin = user.is_superuser or user.groups.filter(name="AdminGroup").exists()
        is_customer = hasattr(user, 'customer_profile') and booking.customer == user.customer_profile
        if not (is_admin or is_customer):
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
        count = Bookings.objects.filter(
            user=user,
            booking_end_time__gte=now,
            status__in=[BookingStatus.NA_CEKANJU, BookingStatus.PRIHVACEN, BookingStatus.ODBIJEN]
        ).count()
        return Response({'count': count})
    # ---------------------------------------------------------------------
    # Endpoint za preuzimanje svih aktivnih rezervacija
    # ---------------------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='active')
    def active_bookings(self, request):
        now_dt = timezone.now()

        active = self.get_queryset().filter(
            Q(status=BookingStatus.ODBIJEN) |  # Sve odbijene bez obzira na datum
            Q(status__in=[BookingStatus.NA_CEKANJU, BookingStatus.PRIHVACEN], booking_end_time__gte=now_dt)  # Aktivne i na čekanju koje nisu prošle
        )

        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)
    # ---------------------------------------------------------------------
    # Endpoint za otkazivanje rezervacije
    # ---------------------------------------------------------------------
    @action(detail=True, methods=["patch"])
    def cancel(self, request, public_id=None):
        booking = self.get_object()

        # Provera statusa
        if booking.status != BookingStatus.NA_CEKANJU:
            return Response({"detail": "Rezervaciju nije moguće otkazati."}, status=400)

        # Provera datuma (7 dana ranije)
        from datetime import datetime, timedelta

        start_datetime = booking.booking_start_time
        if timezone.is_naive(start_datetime):
            start_datetime = make_aware(start_datetime)

        if start_datetime - timezone.now() < timedelta(days=7):
            return Response({"detail": "Rezervaciju je moguće otkazati najkasnije 7 dana unapred."}, status=400)

        # Otkazivanje
        booking.status = BookingStatus.OTKAZAN
        booking.save()

        return Response({"detail": "Rezervacija je uspešno otkazana."}, status=200)