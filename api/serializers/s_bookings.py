from decimal import Decimal
from rest_framework import serializers
from reservations.models import Bookings
from services.models import CustomerServices
from users.models import Children
from datetime import date

# ---------------------------------------------------------------------
# Bookings Serializer
# ---------------------------------------------------------------------
class BookingsSerializer(serializers.ModelSerializer):
    customer_public_id = serializers.CharField(source='customer.public_id', read_only=True)
    location_public_id = serializers.CharField(source='location.public_id', read_only=True)
    user_public_id = serializers.CharField(source='user.public_id', read_only=True)
    location_name = serializers.CharField(source='location.location_name', read_only=True)
    service_name = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    price = serializers.CharField(source='customer_services.price_per_child', read_only=True)
    customer_services = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomerServices.objects.all())
    child = serializers.PrimaryKeyRelatedField(queryset=Children.objects.all(), allow_null=True, required=False)
    child_data = serializers.SerializerMethodField()

    class Meta:
        model = Bookings
        # fields = [
        #     'id', 'public_id', 'customer', 'customer_public_id',
        #     'customer_services', 'service_name',
        #     'location', 'location_public_id', 'location_name',
        #     'user', 'user_public_id', 'status', 'duration',
        #     'booking_date', 'booking_start_time','booking_validation_date',
        #     'booking_end_time','booking_type', 'booking_price','children_count',
        #     'child', 'price', 'description',
        #     'created_at', 'updated_at',
        # ]
        fields = '__all__'
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
    
    def create(self, validated_data):
        services = validated_data.pop('customer_services', [])
        children_count = validated_data.get('children_count')

        # Izračunaj cenu ako je moguće
        if children_count is not None and services:
            total_price_per_child = sum(
                service.price_per_child for service in services if service.price_per_child is not None
            )
            validated_data['booking_price'] = Decimal(children_count) * total_price_per_child

        # Kreiraj instancu Bookings bez M2M
        booking = Bookings.objects.create(**validated_data)

        # Dodeli M2M relaciju (nakon što instanca postoji)
        booking.customer_services.set(services)

        return booking
    
    def get_service_name(self, obj):
        # Ako ima više usluga, prikazati ih spojene zarezom
        services = obj.customer_services.all()
        return ", ".join(service.service_name for service in services)

    def get_duration(self, obj):
        services = obj.customer_services.all()
        total_duration = sum(int(service.duration) for service in services if service.duration and str(service.duration).isdigit())
        return total_duration
    
    def get_child(self, obj):
        from api.serializers.s_user import ChildrenSerializer
        if obj.child:
            return ChildrenSerializer(obj.child).data
        return None
    def get_child_data(self, obj):
        from api.serializers.s_user import ChildrenSerializer
        if obj.child:
            return ChildrenSerializer(obj.child).data
        return None