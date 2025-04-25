from rest_framework import serializers
from playrooms.models import Customer
from users.models import User
from api.serializers.s_user_registration import UserRegistrationSerializer

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = Customer
        fields = [
            'id', 'user', 'name', 'address1', 'address2', 'phone', 'postal_code', 'city',
            'state', 'facebook_url', 'instagram_url', 'customer_url',
            'owner_name', 'owner_lastname', 'owner_email', 'owner_password', 'description'
        ]
        extra_kwargs = {
            'owner_password': {'write_only': True},
            'user': {'required': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['username'] = user_data['email']
        user = UserRegistrationSerializer().create(user_data)
        user.user_type = 'customer'
        user.save()

        customer = Customer.objects.create(
            user=user,
            owner_email=user.email,
            **validated_data
        )
        return customer
