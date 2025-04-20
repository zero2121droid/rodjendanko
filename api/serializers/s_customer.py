from rest_framework import serializers
from playrooms.models import Customer

# ---------------------------------------------------------------------
# Customer Serializer
# ---------------------------------------------------------------------

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'