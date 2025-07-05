from datetime import date, datetime, time, timedelta
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from playrooms.models import Customer, Location, LocationWorkingHours
from reservations.models import Bookings
from api.serializers.s_bookings import BookingsSerializer
from notifications.utils import create_notification
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from reservations.filters import BookingFilter
from django.utils.timezone import now
from django.db.models import Func,F, ExpressionWrapper, DateTimeField, Q
from django.db.models.functions import Cast
from reservations.models import BookingStatus
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_date

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
# Helper function to calculate available slots
# ---------------------------------------------------------------------
def calculate_available_slots(working_hours, bookings, date_obj):
    start_minutes = working_hours.location_opening_time.hour * 60 + working_hours.location_opening_time.minute
    end_minutes = working_hours.location_closing_time.hour * 60 + working_hours.location_closing_time.minute
    duration = working_hours.event_duration * 60  # u minutima
    pause = working_hours.location_brake_duration or 30

    slots = []
    t = start_minutes
    while t + duration <= end_minutes:
        slot_start_time = time(hour=t // 60, minute=t % 60)
        slot_start_dt = datetime.combine(date_obj, slot_start_time)
        slot_end_dt = slot_start_dt + timedelta(minutes=duration)

        is_taken = False
        for booking in bookings:
            if booking.booking_start_time < slot_end_dt and booking.booking_end_time > slot_start_dt:
                is_taken = True
                break

        slots.append({
            "start": slot_start_dt.isoformat(),
            "end": slot_end_dt.isoformat(),
            "taken": is_taken
        })

        t += duration + pause

    return slots

# ---------------------------------------------------------------------
# Bookings ViewSet
# ---------------------------------------------------------------------
class BookingsViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all().select_related('child', 'location', 'user').prefetch_related('customer_services')
    serializer_class = BookingsSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrCustomerOrAdmin]
    lookup_field = 'public_id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["customer__name", "location__location_name", "customer_services__service_name", "booking_date"]
    filterset_fields = ['customer', 'location', 'booking_date', 'status', 'children_count']
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
    
    @action(detail=False, methods=["get"], url_path="my-all", permission_classes=[IsAuthenticated])
    def my_all_bookings(self, request):
        user = request.user

        if user.user_type == 'partner':
            # Partner vidi rezervacije za lokacije koje pripadaju Customer-u gde je on owner
            customers = Customer.objects.filter(owner=user)
            queryset = self.get_queryset().filter(location__customer__in=customers)
        elif user.user_type == 'customer':
            # Customer vidi rezervacije samo za svoje lokacije
            queryset = self.get_queryset().filter(location__customer=user.customer)
        else:
            # Ostali tipovi ne vide rezervacije
            return Response([], status=200)

        # Filteri iz query params (status, year, month, after, before)
        status = request.query_params.get("status")
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        after = request.query_params.get("after")
        before = request.query_params.get("before")

        if status:
            queryset = queryset.filter(status=status)

        if year and year.isdigit():
            queryset = queryset.filter(booking_start_time__year=int(year))

        if month and month.isdigit():
            queryset = queryset.filter(booking_start_time__month=int(month))

        if after:
            after_date = parse_date(after)
            if after_date:
                queryset = queryset.filter(booking_start_time__date__gte=after_date)

        if before:
            before_date = parse_date(before)
            if before_date:
                queryset = queryset.filter(booking_start_time__date__lte=before_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    # ---------------------------------------------------------------------
    # Endpoint za preuzimanje rezervacija po lokaciji
    # ---------------------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='location-bookings', permission_classes=[AllowAny])
    def location_bookings(self, request):
        location_id = request.query_params.get('location_id')
        if not location_id:
            return Response({'detail': 'location_id is required'}, status=400)

        # Uzimamo samo rezervacije koje nisu otkazane
        bookings = Bookings.objects.filter(
            location__public_id=location_id,
            status__in=[BookingStatus.NA_CEKANJU, BookingStatus.PRIHVACEN]
        )

        # Vraćamo samo potrebna polja za frontend
        data = [
            {
                'start': b.booking_start_time.isoformat(),
                'end': b.booking_end_time.isoformat()
            }
            for b in bookings
        ]
        return Response(data)
    # ---------------------------------------------------------------------
    # Endpoint za preuzimanje svih aktivnih rezervacija
    # ---------------------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='active')
    def active_bookings(self, request):
        now_dt = timezone.now()

        active = self.get_queryset().filter(
            booking_end_time__gte=now_dt,
            status__in=[BookingStatus.NA_CEKANJU, BookingStatus.PRIHVACEN, BookingStatus.ODBIJEN]
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
    
    # ---------------------------------------------------------------------
    # Endpoint za preuzimanje slobodnih slotova
    # ---------------------------------------------------------------------

    @action(detail=False, methods=['get'], url_path='available-slots', permission_classes=[])
    def available_slots(self, request):
        location_id = request.query_params.get('location_id')
        date_from_str = request.query_params.get('date_from')
        date_to_str = request.query_params.get('date_to')

        if not date_from_str or not date_to_str:
            return Response({"detail": "date_from i date_to su obavezni"}, status=400)

        date_from = parse_date(date_from_str)
        date_to = parse_date(date_to_str)
        if not date_from or not date_to:
            return Response({"detail": "Nevalidan format datuma"}, status=400)
        if date_from > date_to:
            return Response({"detail": "date_from ne može biti posle date_to"}, status=400)

        # Ako je prosleđen location_id, filtriramo samo jednu lokaciju
        if location_id:
            locations = Location.objects.filter(public_id=location_id)
        else:
            # Inače uzimamo sve lokacije koje imaju definisano radno vreme
            locations = Location.objects.filter(locationworkinghours__isnull=False).distinct()

        result = []

        for location in locations:
            current_date = date_from
            while current_date <= date_to:
                day_of_week = current_date.weekday()

                try:
                    working_hours = LocationWorkingHours.objects.get(location=location, day_of_week=day_of_week)
                except LocationWorkingHours.DoesNotExist:
                    current_date += timedelta(days=1)
                    continue

                bookings = Bookings.objects.filter(
                    location=location,
                    booking_date=current_date,
                    status__in=[BookingStatus.NA_CEKANJU, BookingStatus.PRIHVACEN]
                )

                slots = calculate_available_slots(working_hours, bookings)

                result.append({
                    "location_id": str(location.id),
                    "location_name": location.location_name,
                    "location_city": location.location_city,
                    "date": current_date.isoformat(),
                    "slots": slots
                })

                current_date += timedelta(days=1)

        return Response(result)

    


