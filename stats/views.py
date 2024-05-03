from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    UpdateAPIView,
)
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response

from authentication.authenticator import JWTAuthenticator
from stats.serializers import (
    CartItemListCreateSerializer,
    CartItemUpdateDeleteSerializer,
    SellerSerializer,
)

from .models import CartItem, Seller
from .permissions import IsCorrectCustomer, IsCustomerAndAuthenticated


class SellerListView(ListAPIView):
    serializer_class = SellerSerializer

    def get_queryset(self):
        number = int(self.request.query_params.get("n", 10))
        queryset = Seller.objects.all()[:number]
        return queryset


class CartItemListDeleteView(ListCreateAPIView):
    serializer_class = CartItemListCreateSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsCustomerAndAuthenticated]

    def get_queryset(self):
        customer = self.request.user
        items = CartItem.objects.filter(customer__user=customer)
        return items

    def delete(self, request, *args, **kwargs):
        customer = self.request.user.customer
        cart_items = CartItem.objects.filter(customer=customer)
        cart_items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemDeleteUpdateView(DestroyModelMixin, UpdateAPIView):
    serializer_class = CartItemUpdateDeleteSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsCustomerAndAuthenticated]

    def get_queryset(self):
        customer = self.request.user
        items = CartItem.objects.filter(customer__user=customer)
        return items

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
