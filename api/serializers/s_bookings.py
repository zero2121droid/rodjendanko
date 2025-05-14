from rest_framework import serializers
from reservations.models import Bookings

# ---------------------------------------------------------------------
# Bookings Serializer
# ---------------------------------------------------------------------
class BookingsSerializer(serializers.ModelSerializer):
    customer_public_id = serializers.CharField(source='customer.public_id', read_only=True)
    location_public_id = serializers.CharField(source='location.public_id', read_only=True)
    user_public_id = serializers.CharField(source='user.public_id', read_only=True)
    location_name = serializers.CharField(source='location.location_name', read_only=True)
    service_name = serializers.CharField(source='customer_services.service_name', read_only=True)

    class Meta:
        model = Bookings
        fields = [
            'id', 'public_id', 'customer', 'customer_public_id',
            'customer_services', 'service_name',
            'location', 'location_public_id', 'location_name',
            'user', 'user_public_id', 'status',
            'booking_date', 'booking_start_time','booking_validation_date',
            'booking_end_time','booking_type', 'children_count', 'description',
            'created_at', 'updated_at',
        ]
        read_only_fields = ('id', 'public_id', 'created_at', 'updated_at', 'booking_date', 'booking_validation_date')