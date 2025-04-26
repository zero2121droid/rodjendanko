from rest_framework import serializers
from playrooms.models import Location, LocationImages, LocationWorkingHours

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'public_id', 'location_name', 'address', 'city', 'state', 'postal_code', 'country', 'description', 'latitude', 'longitude']
        extra_kwargs = {
            'public_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        read_only_fields = ['id', 'public_id']

class LocationImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationImages
        fields = '__all__'

class LocationWorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWorkingHours
        fields = '__all__'