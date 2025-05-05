from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.s_user_registration import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from django.utils.timezone import now

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def post(self, request):
        ip_address = self.get_client_ip(request)
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.terms_accepted = True
            user.terms_accepted_at = now()
            user.terms_accepted_ip = ip_address
            user.save()
            return Response({"message": "Uspešna registracija."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
