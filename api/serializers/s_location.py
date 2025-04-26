from rest_framework import serializers
from playrooms.models import Location, LocationImages, LocationWorkingHours

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'public_id', 'customer', 'location_name', 'location_address',
                'description', 'location_latitude', 'location_longitude', 'created_at', 'updated_at']
        extra_kwargs = {
            'public_id': {'read_only': True},
            'customer': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'customer': {'read_only': True},
        }
        read_only_fields = ['id', 'public_id']

class LocationImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationImages
        fields = [
            'id', 'location', 'location_image_url', 'upload_date', 
            'created_at', 'updated_at', 'description'
        ]
        read_only_fields = ['id', 'upload_date', 'created_at', 'updated_at']

class LocationWorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWorkingHours
        fields = [
            'id', 'location', 'day_of_week', 'location_opening_time', 
            'location_closing_time', 'location_brake_duration', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']