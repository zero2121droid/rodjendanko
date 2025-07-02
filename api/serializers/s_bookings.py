from decimal import Decimal
from rest_framework import serializers
from reservations.models import Bookings, BookingStatus
from services.models import CustomerServices
from users.models import Children
from datetime import date
from reservations.models import Rating
from rest_framework.exceptions import ValidationError


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
    rating = serializers.SerializerMethodField()

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
    
    
    def validate(self, data):
        # Ako je update, proveri da li menjamo vreme
        instance = getattr(self, 'instance', None)

        start_time = data.get('booking_start_time', getattr(instance, 'booking_start_time', None))
        end_time = data.get('booking_end_time', getattr(instance, 'booking_end_time', None))
        location = data.get('location', getattr(instance, 'location', None))

        if not (start_time and end_time and location):
            return data  # preskoči ako podaci nisu svi prisutni

        overlapping = Bookings.objects.filter(
            location=location,
            booking_start_time__lt=end_time,
            booking_end_time__gt=start_time,
            status__in=[BookingStatus.NA_CEKANJU, BookingStatus.PRIHVACEN]
        )

        # Ako je update, isključi sebe
        if instance:
            overlapping = overlapping.exclude(pk=instance.pk)

        if overlapping.exists():
            raise ValidationError("Izabrani termin je već rezervisan.")
        
        return data
    
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
    
    def get_rating(self, obj):
        rating = Rating.objects.filter(booking=obj).first()
        return rating.rating if rating else None