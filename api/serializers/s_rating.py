from rest_framework import serializers
from reservations.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'location', 'booking', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
