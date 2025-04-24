from rest_framework import viewsets, filters, status
from users.models import User, Children
from api.serializers.s_user import UserSerializer, ChildrenSerializer
from api.serializers.s_user_registration import UserRegistrationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers.s_user import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email", "city", "phone"]
    filterset_fields = ["city", "coins_wallet"]  
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        elif user.is_staff:
            return User.objects.filter(is_staff=False)
        else:
            return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Endpoint za registraciju novog korisnika
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'Korisnik uspešno registrovan',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ChildrenViewSet(viewsets.ModelViewSet):
    serializer_class = ChildrenSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["username"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Children.objects.all()
        return Children.objects.filter(user=user)
    
  
