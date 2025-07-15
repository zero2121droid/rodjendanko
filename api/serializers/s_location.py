from rest_framework import serializers
from playrooms.models import Location, LocationImages, LocationWorkingHours

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        extra_kwargs = {
            'public_id': {'read_only': True},
            'customer': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'customer': {'read_only': True},
        }
        read_only_fields = ['id', 'public_id']

class LocationImagesSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = LocationImages
        fields = "__all__"
        read_only_fields = ['id', 'upload_date', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.location_image:
            return obj.location_image.url
        return None

class LocationWorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWorkingHours
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']