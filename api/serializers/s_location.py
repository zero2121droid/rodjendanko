from rest_framework import serializers
from playrooms.models import Location, LocationImages, LocationWorkingHours, LocationCity

class LocationSerializer(serializers.ModelSerializer):
    location_city = serializers.PrimaryKeyRelatedField(
        queryset=LocationCity.objects.all(),
        allow_null=True,
        required=False
    )
    location_city_name = serializers.CharField(source='location_city.city_name', read_only=True)

    class Meta:
        model = Location
        fields = "__all__"
        extra_kwargs = {
            'public_id': {'read_only': True},
            'customer': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
        read_only_fields = ['id', 'public_id']
    
    def validate_location_accommodation_children_aged(self, value):
        valid_choices = ['0-3', '4-7', '8-12', '13+']
        if value and isinstance(value, list):
            for choice in value:
                if choice not in valid_choices:
                    raise serializers.ValidationError(f"Nepravilan izbor: {choice}")
        return value
    
    def validate(self, data):
        """Validacija min/max children polja"""
        min_children = data.get('location_min_children')
        max_children = data.get('location_max_children')
        
        if min_children is not None and min_children < 1:
            raise serializers.ValidationError("Minimalni broj dece mora biti veći od 0")
            
        if max_children is not None and max_children < 1:
            raise serializers.ValidationError("Maksimalni broj dece mora biti veći od 0")
            
        if min_children is not None and max_children is not None:
            if min_children > max_children:
                raise serializers.ValidationError("Minimalni broj dece ne može biti veći od maksimalnog")
                
        return data

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

class LocationCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCity
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']