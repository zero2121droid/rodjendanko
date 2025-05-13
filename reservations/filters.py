import django_filters
from reservations.models import Bookings, BookingStatus

class BookingFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=[(status.value, status.label) for status in BookingStatus]
    )

    class Meta:
        model = Bookings
        fields = ['customer', 'location', 'booking_date', 'status']
