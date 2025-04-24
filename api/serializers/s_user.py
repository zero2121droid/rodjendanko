from rest_framework import serializers
from users.models import User, Children
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.serializers.s_bookings import BookingsSerializer

# ---------------------------------------------------------------------
# Children Serializer
# ---------------------------------------------------------------------

class ChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Children
        fields = '__all__'

# ---------------------------------------------------------------------
# Users Serializer
# ---------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    children = ChildrenSerializer(many=True, read_only=True, source='children_set')
    bookings = BookingsSerializer(many=True, read_only=True, source='bookings_set')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name','address', 'city', 'phone', 'email',
            'password', 'coins_wallet', 'bookings','description', 'created_at', 'updated_at', 'children'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'coins_wallet': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email adresa vec postoji.")
        return value
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # dodatna polja u token ako želiš
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # override default validacije da koristi email
        username_field = User.EMAIL_FIELD
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)
# ---------------------------------------------------------------------

