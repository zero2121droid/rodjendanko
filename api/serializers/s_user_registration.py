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
        # Ukloni 'password2' jer nije potreban za kreiranje korisnika
        validated_data.pop('password2')  
        password = validated_data.pop('password')

        # Kreiraj korisnika
        user = User(**validated_data)
        user.set_password(password)
        user.save()  # Spasi korisnika pre nego što kreiraš wallet

        # Kreiraj wallet za korisnika i postavi početni broj coina
        from wallet.models import CoinsWallet
        wallet = CoinsWallet.objects.create(user=user, coins_balance=100)  # Početni iznos je 100
        user.coins_wallet = wallet  # Poveži wallet sa korisnikom
        user.save()  # Sačuvaj korisnika sa povezanim wallet-om

        return user
