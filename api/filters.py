import django_filters
from django.db import models
from playrooms.models import Location

class LocationFilter(django_filters.FilterSet):
    """
    Custom filter za Location model koji pravilno rukuje JSONField
    """
    # Eksplicitno definiši filter za location_accommodation_children_aged
    location_accommodation_children_aged = django_filters.CharFilter(
        field_name='location_accommodation_children_aged',
        lookup_expr='icontains',
        help_text="Filter by age ranges in JSON field"
    )
    
    class Meta:
        model = Location
        fields = [
            "customer", 
            "location_city", 
            "location_type",
            "location_accommodation_wifi",
            "location_accommodation_videosurveillance",
            "location_accommodation_air_conditioning",
            "location_accommodation_animator",
            "location_accommodation_catering",
            "location_accommodation_parking",
            "location_featured",
            "location_top_priority",
            "location_min_children",
            "location_max_children"
        ]
        
        # Override za JSONField
        filter_overrides = {
            models.JSONField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }