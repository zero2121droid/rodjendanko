from rest_framework import serializers
from users.models import User, Children

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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'name', 'last_name', 'address', 'city', 'phone', 'email',
            'password', 'coins', 'description', 'created_at', 'updated_at', 'children'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

