import uuid
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from services.models import CustomerServices, PartnerServices, OtherServices, ServicesImages
from api.serializers.s_services import CustomerServicesSerializer, PartnerServicesSerializer, OtherServicesSerializer, ServicesImagesSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

# ---------------------------------------------------------------------
# Customer Services ViewSet
# ---------------------------------------------------------------------
class CustomerServicesViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerServicesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["service_name", "service_type", "description"]
    #filterset_fields = ["service_type", "location"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        location_param = self.request.query_params.get("location")
        queryset = CustomerServices.objects.all()

        if location_param:
            try:
                uuid_obj = uuid.UUID(location_param)
                queryset = queryset.filter(location__id=uuid_obj)
            except ValueError:
                queryset = queryset.filter(location__public_id=location_param)

        service_param = self.request.query_params.get("service")
        if service_param:
            try:
                uuid_obj = uuid.UUID(service_param)
                queryset = queryset.filter(id=uuid_obj)
            except ValueError:
                queryset = queryset.filter(public_id=service_param)

        return queryset.order_by("created_at")
# ---------------------------------------------------------------------
# Partner Services ViewSet
# ---------------------------------------------------------------------
class PartnerServicesViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerServicesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["product_name", "description", "customer"]
    filterset_fields = ["customer"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]  # defaultno sortiranje po created_at
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="AdminGroup").exists() or user.is_superuser:
            return PartnerServices.objects.all().order_by("created_at")
        return PartnerServices.objects.filter(customer__user=user).order_by("created_at")
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
            return OtherServices.objects.all().order_by("created_at")
        return OtherServices.objects.filter(customer__user=user).order_by("created_at")
# ---------------------------------------------------------------------
# Services Images ViewSet
# ---------------------------------------------------------------------
class ServicesImagesViewSet(viewsets.ModelViewSet):
    serializer_class = ServicesImagesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["service_type", "service_id"]
    filterset_fields = ["service_type"]  # primer za precizno filtriranje
    ordering_fields = ["upload_date", "created_at", "updated_at"]
    ordering = ["upload_date"]  # defaultno sortiranje po upload_date
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="AdminGroup").exists() or user.is_superuser:
            return ServicesImages.objects.all().order_by("created_at")
        return ServicesImages.objects.none().order_by("created_at")
# ---------------------------------------------------------------------