from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from services.models import CustomerServices, PartnerServices, OtherServices, ServicesImages
from api.serializers.s_services import CustomerServicesSerializer, PartnerServicesSerializer, OtherServicesSerializer, ServicesImagesSerializer

# ---------------------------------------------------------------------
# Customer Services ViewSet
# ---------------------------------------------------------------------
class CustomerServicesViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerServicesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["service_name", "service_type", "description"]
    filterset_fields = ["service_type", "location"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomerServices.objects.all()
        return CustomerServices.objects.filter(location__customer__user=user)
# ---------------------------------------------------------------------
# Partner Services ViewSet
# ---------------------------------------------------------------------
class PartnerServicesViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerServicesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["product_name", "description", "customer"]
    filterset_fields = ["customer"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PartnerServices.objects.all()
        return PartnerServices.objects.filter(customer__user=user)
# ---------------------------------------------------------------------
# Other Services ViewSet
# ---------------------------------------------------------------------
class OtherServicesViewSet(viewsets.ModelViewSet):
    serializer_class = OtherServicesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "customer"]
    filterset_fields = ["customer"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OtherServices.objects.all()
        return OtherServices.objects.filter(customer__user=user)
# ---------------------------------------------------------------------
# Services Images ViewSet
# ---------------------------------------------------------------------
class ServicesImagesViewSet(viewsets.ModelViewSet):
    serializer_class = ServicesImagesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["service_type", "service_id"]
    filterset_fields = ["service_type"]  # primer za precizno filtriranje
    ordering_fields = ["upload_date", "created_at", "updated_at"]
    ordering = ["upload_date"]  # defaultno sortiranje po upload_date
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ServicesImages.objects.all()
        return ServicesImages.objects.none()
# ---------------------------------------------------------------------