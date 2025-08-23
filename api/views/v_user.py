from rest_framework import viewsets, filters, status
from users.models import User, Children
from api.serializers.s_user import UserSerializer, ChildrenSerializer
from api.serializers.s_user_registration import UserRegistrationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers.s_user import CustomTokenObtainPairSerializer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from users.permissions import IsOwnerOrAdmin
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from services.brevo_service import add_contact_to_brevo


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email", "city", "phone"]
    filterset_fields = ["city", "coins_wallet"]  
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="AdminGroup").exists() or user.is_superuser:
            return User.objects.all().order_by("created_at")
        elif user.is_staff:
            return User.objects.filter(is_staff=False).order_by("created_at")
        else:
            return User.objects.filter(id=user.id).order_by("created_at")
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            add_contact_to_brevo(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name
            )
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

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def google_login(self, request):
        """
        Endpoint za prijavu korisnika pomoću Google ID tokena
        """
        token = request.data.get('id_token')
        if not token:
            return Response({'error': 'id_token je obavezan'}, status=400)

        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': get_random_string(32)
            })

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'created': created
            })

        except Exception as e:
            return Response({'error': 'Nevalidan token', 'detalji': str(e)}, status=400)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        target_user = self.get_object()

        if 'is_active' in request.data and not (
            user.is_superuser or user.groups.filter(name="AdminGroup").exists()
        ):
            return Response(
                {'detail': 'Nemate dozvolu da menjate aktivnost korisnika.'},
                status=403
            )

        return super().update(request, *args, **kwargs)

class ChildrenViewSet(viewsets.ModelViewSet):
    serializer_class = ChildrenSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]
    parser_classes = [JSONParser,MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="AdminGroup").exists() or user.is_superuser:
            return Children.objects.all().order_by("created_at")
        return Children.objects.filter(user=user).order_by("created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
  
