from rest_framework import serializers
from services.models import CustomerServices, PartnerServices, OtherServices, ServicesImages

class CustomerServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerServices
        fields = '__all__'

class PartnerServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerServices
        fields = '__all__'

class OtherServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherServices
        fields = '__all__'

class ServicesImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesImages
        fields = '__all__'