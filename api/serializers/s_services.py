from rest_framework import serializers
from services.models import CustomerServices, PartnerServices, OtherServices, ServicesImages

class CustomerServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerServices
        fields = '__all__'
        #fields = ('id', 'customer', 'service_name', 'description', 'price_per_child', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class PartnerServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerServices
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class OtherServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherServices
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class ServicesImagesSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()
    class Meta:
        model = ServicesImages
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_fields = ['service_name']  # dodatno prikazujemo ime

    def get_service_name(self, obj):
        if obj.content_object:
            # Proveravamo redom koji atribut postoji
            return (
                getattr(obj.content_object, 'service_name', None) or
                getattr(obj.content_object, 'product_name', None) or
                getattr(obj.content_object, 'name', None)
            )
        return None