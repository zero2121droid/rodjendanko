from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from services.models import CustomerServices, PartnerServices, OtherServices, ServicesImages
from api.serializers.s_services import CustomerServicesSerializer, PartnerServicesSerializer, OtherServicesSerializer, ServicesImagesSerializer

# ---------------------------------------------------------------------
# Customer Services ViewSet
# ---------------------------------------------------------------------
class CustomerServicesViewSet(viewsets.ModelViewSet):
    queryset = CustomerServices.objects.all()
    serializer_class = CustomerServicesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["service_name", "service_type", "description", "location"]
    filterset_fields = ["service_type", "location"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
# ---------------------------------------------------------------------
# Partner Services ViewSet
# ---------------------------------------------------------------------
class PartnerServicesViewSet(viewsets.ModelViewSet):
    queryset = PartnerServices.objects.all()
    serializer_class = PartnerServicesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["product_name", "description", "customer"]
    filterset_fields = ["customer"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
# ---------------------------------------------------------------------
# Other Services ViewSet
# ---------------------------------------------------------------------
class OtherServicesViewSet(viewsets.ModelViewSet):
    queryset = OtherServices.objects.all()
    serializer_class = OtherServicesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "customer"]
    filterset_fields = ["customer"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
# ---------------------------------------------------------------------
# Services Images ViewSet
# ---------------------------------------------------------------------
class ServicesImagesViewSet(viewsets.ModelViewSet):
    queryset = ServicesImages.objects.all()
    serializer_class = ServicesImagesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["service_type", "service_id"]
    filterset_fields = ["service_type"]  # primer za precizno filtriranje
    ordering_fields = ["upload_date", "created_at", "updated_at"]
    ordering = ["upload_date"]  # defaultno sortiranje po upload_date
# ---------------------------------------------------------------------