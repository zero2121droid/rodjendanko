import uuid
from django.forms import ValidationError
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from playrooms.models import Customer, Location, LocationImages, LocationWorkingHours
from api.serializers.s_location import LocationSerializer, LocationImagesSerializer, LocationWorkingHoursSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
# ---------------------------------------------------------------------
# Location ViewSet
# ---------------------------------------------------------------------
class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_name", "location_address", "description"]
    filterset_fields = ["customer"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        return Location.objects.all()
    # partner da vidi samo svoje lokacije, takodje za partnere u response da se vracaju svi bookingsi bez paginacije, dodati polje start date i end date za filtere
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=["get"], url_path="my", permission_classes=[IsAuthenticated])
    def my_locations(self, request):
        user = request.user

        if user.user_type == 'partner':
            customers = Customer.objects.filter(owner=user)
            queryset = Location.objects.filter(customer__in=customers)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        elif hasattr(user, "customer"):
            queryset = Location.objects.filter(customer=user.customer)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response([], status=200)
    # -------------------------------------------------
    # Ova funkcija perform_update se poziva kada se kreira nova lokacija.
    # Kada frontend pošalje POST request za kreiranje lokacije, NE šalje customer.
    # Backend u perform_create() proveri koji customer pripada ulogovanom korisniku (user.customer_profile).
    # Ako postoji, automatski ga ubaci u snimanje (serializer.save(customer=customer)).
    # Ako ne postoji, vrati grešku da user nema Customer (što bi inače značilo da nije Owner ili je neki problem).
    # -------------------------------------------------
    def perform_create(self, serializer):
        user = self.request.user
        try:
            customer = user.customer_profile
        except Customer.DoesNotExist:
            raise ValidationError("Niste povezani ni sa jednom igraonicom.")

        serializer.save(customer=customer)
# ---------------------------------------------------------------------
# Location Images ViewSet
# --------------------------------------------------------------------- 
class LocationImagesViewSet(viewsets.ModelViewSet):
    serializer_class = LocationImagesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_image_url", "description"]
    filterset_fields = ["location"]  # primer za precizno filtriranje
    ordering_fields = ["upload_date", "created_at", "updated_at"]
    ordering = ["upload_date"]  # defaultno sortiranje po upload_date

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="AdminGroup").exists() or user.is_superuser:
            return LocationImages.objects.all()
        return LocationImages.objects.filter(location__customer__user=user) 
    
    def perform_create(self, serializer):
        user = self.request.user
        location_id = self.request.data.get('location')
        if not location_id:
            raise ValidationError("Location ID is required.")

        try:
            location = Location.objects.get(id=location_id, customer__user=user)
        except Location.DoesNotExist:
            raise ValidationError("Location not found or you don't have permission.")

        serializer.save(location=location)
# ---------------------------------------------------------------------
# Location Working Hours ViewSet
# ---------------------------------------------------------------------
class LocationWorkingHoursViewSet(viewsets.ModelViewSet):
    serializer_class = LocationWorkingHoursSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]  # samo za testiranje
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_opening_time", "location_closing_time", "location_brake_duration"]
    #filterset_fields = ["location"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        location_param = self.request.query_params.get("location")

        if location_param:
            try:
                uuid_obj = uuid.UUID(location_param)
                return LocationWorkingHours.objects.filter(location__id=uuid_obj).order_by("created_at")
            except ValueError:
                return LocationWorkingHours.objects.filter(location__public_id=location_param).order_by("created_at")

        return LocationWorkingHours.objects.all().order_by("created_at")

    def perform_create(self, serializer):
        user = self.request.user
        location_id = self.request.data.get('location')
        if not location_id:
            raise ValidationError("Location ID is required.")

        try:
            location = Location.objects.get(id=location_id, customer__user=user)
        except Location.DoesNotExist:
            raise ValidationError("Location not found or you don't have permission.")

        serializer.save(location=location)
# ---------------------------------------------------------------------