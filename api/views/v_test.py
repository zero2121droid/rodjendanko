from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone

class TestPublicView(APIView):
    """
    Test endpoint za proveravanje da li javni pristup radi
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        return Response({
            "message": "Javni pristup radi!",
            "user_authenticated": request.user.is_authenticated if hasattr(request, 'user') else False,
            "timestamp": timezone.now().isoformat()
        })
