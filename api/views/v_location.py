from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from playrooms.models import Location, LocationImages, LocationWorkingHours
from api.serializers.s_location import LocationSerializer, LocationImagesSerializer, LocationWorkingHoursSerializer
# ---------------------------------------------------------------------
# Location ViewSet
# ---------------------------------------------------------------------
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_name", "location_address", "description"]
    filterset_fields = ["customer"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updates_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
# ---------------------------------------------------------------------
# Location Images ViewSet
# --------------------------------------------------------------------- 
class LocationImagesViewSet(viewsets.ModelViewSet):
    queryset = LocationImages.objects.all()
    serializer_class = LocationImagesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_image_url", "description"]
    filterset_fields = ["location"]  # primer za precizno filtriranje
    ordering_fields = ["upload_date", "created_at", "updated_at"]
    ordering = ["upload_date"]  # defaultno sortiranje po upload_date
# ---------------------------------------------------------------------
# Location Working Hours ViewSet
# ---------------------------------------------------------------------
class LocationWorkingHoursViewSet(viewsets.ModelViewSet):
    queryset = LocationWorkingHours.objects.all()
    serializer_class = LocationWorkingHoursSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location_opening_time", "location_closing_time", "location_brake_duration"]
    filterset_fields = ["location"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
# ---------------------------------------------------------------------