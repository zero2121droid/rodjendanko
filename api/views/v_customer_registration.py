from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.s_customer_registration import CustomerRegistrationSerializer
from rest_framework.permissions import AllowAny

class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(CustomerRegistrationSerializer(customer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
