import django_filters
from reservations.models import Bookings, BookingStatus

class BookingFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=BookingStatus.choices)
    booking_date = django_filters.DateFilter(field_name='booking_date', lookup_expr='date')

    class Meta:
        model = Bookings
        fields = ['customer', 'location', 'booking_date', 'status']
