from rest_framework import serializers
from playrooms.models import Location, LocationImages, LocationWorkingHours

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationImages
        fields = '__all__'

class LocationWorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWorkingHours
        fields = '__all__'