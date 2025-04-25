from rest_framework import serializers
from playrooms.models import Customer
from users.models import User
from api.serializers.s_user_registration import UserRegistrationSerializer
from wallet.models import CoinsWallet

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

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
        user_data = validated_data.pop("user")

        # 1. Kreiraj user-a sa svim potrebnim podacima
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # 2. Kreiraj wallet samo ako ne postoji
        CoinsWallet.objects.get_or_create(user=user, defaults={"coins_balance": 100})

        # 3. Kreiraj customera sa povezanim korisnikom
        customer = Customer.objects.create(user=user, **validated_data)

        return customer
