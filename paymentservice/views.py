from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.authenticator import JWTAuthenticator

from .models import Order
from .serializers import OrderSerializer


class ViewPerformOrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = self.request.user.customer
        return Order.objects.filter(customer=customer)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["customer"] = self.request.user.customer
        return context


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = self.request.user.customer
        return Order.objects.filter(customer=customer)
