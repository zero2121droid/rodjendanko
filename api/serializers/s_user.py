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
        read_only_fields = ['years', 'created_at', 'updated_at']
    
    def get_years(self, obj):
        return obj.years

# ---------------------------------------------------------------------
# Users Serializer
# ---------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    children = ChildrenSerializer(many=True, read_only=True)
    bookings = BookingsSerializer(many=True, read_only=True, source='bookings_set')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'public_id', 'username', 'first_name', 'last_name','address', 'city', 'phone', 'email',
            'password', 'coins_wallet', 'bookings','description', 'created_at', 'updated_at', 'children', 'owner', 'is_active', 'user_type'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'coins_wallet': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if User.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError("Email adresa već postoji.")
        return value
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def get_customer_id(self, obj):
        if obj.user_type == 'partner' and hasattr(obj, 'customer'):
            return obj.customer.id
        return None
    
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

