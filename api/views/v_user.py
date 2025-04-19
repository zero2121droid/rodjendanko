from rest_framework import viewsets, filters
from users.models import User, Children
from api.serializers.s_user import UserSerializer, ChildrenSerializer
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "last_name", "email", "city", "phone"]
    filterset_fields = ["city", "coins"]  # primer za precizno filtriranje
    ordering_fields = ["created_at", "updated_at"]

class ChildrenViewSet(viewsets.ModelViewSet):
    queryset = Children.objects.all()
    serializer_class = ChildrenSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["user"]
