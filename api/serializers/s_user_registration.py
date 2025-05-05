from datetime import timezone
from rest_framework import serializers
from users.models import User
from playrooms.models import Customer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})  # za potvrdu lozinke
    terms_accepted = serializers.BooleanField(write_only=True)
    

    class Meta:
        model = User
        fields = ['username','email', 'password', 'password2', 'address', 'city', 'phone', 'description', 'terms_accepted', 'user_type', 'company_name', 'owner']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email adresa već postoji.")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Lozinke se ne poklapaju."})
        if not attrs.get('terms_accepted'):
            raise serializers.ValidationError({"terms_accepted": "Morate prihvatiti uslove korišćenja."})
        if attrs.get("user_type") == "partner" and not attrs.get("company_name"):
            raise serializers.ValidationError({"company_name": "Naziv firme je obavezan za partnere."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Uklanjamo potvrdu lozinke
        terms_accepted = validated_data.pop('terms_accepted')
        password = validated_data.pop('password')
        user_type = serializers.ChoiceField(choices=User.USER_TYPES)
        company_name = serializers.CharField(required=False, allow_blank=True)

        request = self.context.get('request')  # Dohvati request iz konteksta
        ip_address = None
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        user = User(**validated_data)
        user.set_password(password)  # Hash-uj lozinku
        user.user_type = 'user' 
        user.terms_accepted = terms_accepted
        user.terms_accepted_at = timezone.now()
        user.terms_accepted_ip = ip_address
        user.save()
        
        if user_type == "partner" and company_name:
            Customer.objects.create(user=user, name=company_name)
        return user