from rest_framework import serializers
from playrooms.models import Customer

# ---------------------------------------------------------------------
# Customer Serializer
# ---------------------------------------------------------------------

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'public_id', 'name', 'email', 'phone_number', 'address', 'city', 'state', 'postal_code', 'country', 'description']
        extra_kwargs = {
            'public_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        read_only_fields = ['id', 'public_id']