from rest_framework import serializers
from users.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})  # za potvrdu lozinke

    class Meta:
        model = User
        fields = ['username','email', 'password', 'password2', 'address','city', 'phone', 'description']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email adresa već postoji.")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Lozinke se ne poklapaju."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Uklanjamo potvrdu lozinke
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash-uj lozinku
        user.user_type = 'user' 
        user.save()
        return user