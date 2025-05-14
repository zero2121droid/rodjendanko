from django_filters import rest_framework as filters
from reservations.models import Bookings, BookingStatus

class BookingFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=BookingStatus.choices)

    class Meta:
        model = Bookings
        fields = ['customer', 'location', 'booking_date', 'status']
