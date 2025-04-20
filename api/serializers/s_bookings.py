from rest_framework import serializers
from reservations.models import Bookings

# ---------------------------------------------------------------------
# Bookings Serializer
# ---------------------------------------------------------------------
class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'