from rest_framework import serializers
from playrooms.models import Customer

# ---------------------------------------------------------------------
# Customer Serializer
# ---------------------------------------------------------------------

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'public_id', 'user', 'name', 'address', 'phone', 'postal_code', 'city', 'state',
                    'facebook_url', 'instagram_url', 'customer_url',
                    'owner_name', 'owner_lastname', 'owner_email',
                    'description', 'created_at', 'updated_at']
        extra_kwargs = {
            'public_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'user': {'read_only': True},
        }
        read_only_fields = ['id', 'public_id']