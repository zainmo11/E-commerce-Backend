from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView, Response

from stats.serializers import SellerSerializer

from .authenticator import JWTAuthenticator, JWToken
from .serializers import CredientalsSerializer, UserSerializer


class AuthenticateUserView(APIView):
    serializer_class = CredientalsSerializer

    def post(self, request):
        user_credientals = self.serializer_class(data=request.data)
        if user_credientals.is_valid():
            email = user_credientals.validated_data["email"]
            password = user_credientals.validated_data["password"]
            access_token = JWToken.get_for_user(email, password)

            return Response({"token": str(access_token)})

        return Response({"details": "Invalid form"}, status=HTTP_406_NOT_ACCEPTABLE)


class RegisterUserView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response(status=HTTP_201_CREATED)

        return Response({"details": "Invalid form"}, status=HTTP_406_NOT_ACCEPTABLE)


class RegisterSellerView(generics.CreateAPIView):
    serializer_class = SellerSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]


class DummyView(APIView):
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {"details": "Hello, this is a restricted end point"}

        return Response(content)
