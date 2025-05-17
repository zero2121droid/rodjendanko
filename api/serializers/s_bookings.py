from rest_framework import serializers
from reservations.models import Bookings
from users.models import Children
from datetime import date
from api.serializers.s_user import ChildrenSerializer

# ---------------------------------------------------------------------
# Bookings Serializer
# ---------------------------------------------------------------------
class BookingsSerializer(serializers.ModelSerializer):
    customer_public_id = serializers.CharField(source='customer.public_id', read_only=True)
    location_public_id = serializers.CharField(source='location.public_id', read_only=True)
    user_public_id = serializers.CharField(source='user.public_id', read_only=True)
    location_name = serializers.CharField(source='location.location_name', read_only=True)
    service_name = serializers.CharField(source='customer_services.service_name', read_only=True)
    duration = serializers.CharField(source='customer_services.duration', read_only=True)
    price = serializers.CharField(source='customer_services.price_per_child', read_only=True)
    child = ChildrenSerializer(read_only=True)


    class Meta:
        model = Bookings
        fields = [
            'id', 'public_id', 'customer', 'customer_public_id',
            'customer_services', 'service_name',
            'location', 'location_public_id', 'location_name',
            'user', 'user_public_id', 'status', 'duration',
            'booking_date', 'booking_start_time','booking_validation_date',
            'booking_end_time','booking_type', 'booking_price','children_count',
            'child', 'price', 'description',
            'created_at', 'updated_at',
        ]
        read_only_fields = (
            'id', 'public_id', 'booking_price','created_at', 'updated_at',
            'booking_date', 'booking_validation_date'
        )
    
    def get_child_bday(self, obj):
        if obj.child and obj.child.birth_date:
            today = date.today()
            age = today.year - obj.child.birth_date.year - (
                (today.month, today.day) < (obj.child.birth_date.month, obj.child.birth_date.day)
            )
            return age
        return None