from rest_framework import serializers
from playrooms.models import Customer
from users.models import User
from api.serializers.s_user_registration import UserRegistrationSerializer

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()  # Koristi serializer za User model

    class Meta:
        model = Customer
        fields = [
            'id', 'user', 'name', 'address1', 'address2', 'phone', 'postal_code', 'city',
            'state', 'facebook_url', 'instagram_url', 'customer_url',
            'owner_name', 'owner_lastname', 'description'
        ]
        extra_kwargs = {
            'user': {'required': True},
        }

    def create(self, validated_data):
        # Ekstraktujemo podatke o korisniku
        user_data = validated_data.pop('user')

        # Korisnik dobija email kao username
        user_data['username'] = user_data['email']

        # Kreiramo korisnika (vlasnika)
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Kreiramo Customer (igraonicu) i povezujemo je sa korisnikom
        customer = Customer.objects.create(
            user=user,  # povezujemo korisnika sa igraonicom
            **validated_data
        )

        return customer
