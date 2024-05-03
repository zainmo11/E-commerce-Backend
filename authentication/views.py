from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView, Response

from stats.models import Customer
from stats.serializers import CustomerRegistrationSerializer, SellerSerializer

from .authenticator import JWTAuthenticator, JWToken
from .serializers import CredientalsSerializer, UserSerializer

User = get_user_model()


class AuthenticateUserView(APIView):
    serializer_class = CredientalsSerializer

    def post(self, request):
        user_credientals = self.serializer_class(data=request.data)
        if user_credientals.is_valid():
            email = user_credientals.validated_data["email"]
            password = user_credientals.validated_data["password"]
            access_token = JWToken.get_for_user(email, password)

            user = User.objects.get(email=email)
            user_serializer = UserSerializer(user)

            return Response({"token": str(access_token), "user": user_serializer.data})

        return Response({"details": "Invalid form"}, status=HTTP_406_NOT_ACCEPTABLE)


class RegisterCustomerView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    queryset = Customer.objects.all()


class RegisterSellerView(generics.CreateAPIView):
    serializer_class = SellerSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        seller_group = Group.objects.get(name="Sellers")
        request.user.groups.add(seller_group)

        return super().post(request, *args, **kwargs)
