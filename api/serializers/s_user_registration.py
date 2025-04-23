from rest_framework import serializers
from users.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})  # za potvrdu lozinke

    class Meta:
        model = User
        fields = ['username','email', 'password', 'password2', 'address','city', 'phone', 'description']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email adresa već postoji.")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Lozinke se ne poklapaju."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # ne treba za kreiranje korisnika
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        from wallet.models import CoinsWallet
        wallet = CoinsWallet.objects.create(user=user, coins_balance=100)  # Početni iznos je 100
        user.coins_wallet = wallet
        user.save()
        return user
