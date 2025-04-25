from rest_framework import serializers
from playrooms.models import Customer
from users.models import User
from api.serializers.s_user_registration import UserRegistrationSerializer

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'coins']
        extra_kwargs = {
            'user': {'required': True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['username'] = user_data['email']  # ako koristiš email kao username
        user = UserRegistrationSerializer().create(user_data)
        user.user_type = 'customer'  # ako imaš `user_type` polje
        user.save()

        customer = Customer.objects.create(user=user, owner_email=user.email, **validated_data)
        return customer
    
    def to_representation(self, instance): # vraća sve podatke o korisniku
        rep = super().to_representation(instance)
        rep['user'] = UserRegistrationSerializer(instance.user).data
        return rep
