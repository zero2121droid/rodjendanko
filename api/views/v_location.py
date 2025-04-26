from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from playrooms.models import Location, LocationImages, LocationWorkingHours
from api.serializers.s_location import LocationSerializer, LocationImagesSerializer, LocationWorkingHoursSerializer
# ---------------------------------------------------------------------
# Location ViewSet
# ---------------------------------------------------------------------
class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_name", "location_address", "description"]
    filterset_fields = ["customer"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updates_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Location.objects.all()
        return Location.objects.filter(customer__user=user)  # filtriraj po korisniku koji je vlasnik lokacije
# ---------------------------------------------------------------------
# Location Images ViewSet
# --------------------------------------------------------------------- 
class LocationImagesViewSet(viewsets.ModelViewSet):
    serializer_class = LocationImagesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_image_url", "description"]
    filterset_fields = ["location"]  # primer za precizno filtriranje
    ordering_fields = ["upload_date", "created_at", "updated_at"]
    ordering = ["upload_date"]  # defaultno sortiranje po upload_date

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LocationImages.objects.all()
        return LocationImages.objects.filter(location__customer__user=user) 
# ---------------------------------------------------------------------
# Location Working Hours ViewSet
# ---------------------------------------------------------------------
class LocationWorkingHoursViewSet(viewsets.ModelViewSet):
    serializer_class = LocationWorkingHoursSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_opening_time", "location_closing_time", "location_brake_duration"]
    filterset_fields = ["location"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LocationWorkingHours.objects.all()
        return LocationWorkingHours.objects.filter(location__customer__user=user)
# ---------------------------------------------------------------------