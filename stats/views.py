from rest_framework import generics, status
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.authenticator import JWTAuthenticator
from store.models import Product
from store.permissions import IsSeller
from store.serializers import PrivateProductSerializer, ProductSerializer

from .models import CartItem, Customer, Seller
from .serializers import (
    CartItemListCreateSerializer,
    CartItemUpdateDeleteSerializer,
    PrivateSellerSerializer,
    SellerSerializer,
    WishlistProductSerializer,
)


class SellerListView(generics.ListAPIView):
    serializer_class = SellerSerializer

    def get_queryset(self):
        number = int(self.request.query_params.get("n", 10))
        queryset = Seller.objects.all()[:number]
        return queryset


class PrivateSellerInfoView(generics.RetrieveAPIView):
    queryset = Seller.objects.all().select_related("user")
    serializer_class = PrivateSellerSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsSeller]

    def get_object(self):
        user = self.request.user
        return self.queryset.get(user=user)


class LowOnStockProductsView(generics.ListAPIView):
    serializer_class = PrivateProductSerializer

    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsSeller]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(seller__user=user, quantity__lte=5)


class AddProductToWishlistView(APIView):
    serializer_class = WishlistProductSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class RemoveProductWishlistView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.customer = self.request.user.customer
        self.wishlist = self.customer.wishlist
        return self.wishlist

    def perform_destroy(self, instance):
        self.wishlist.remove(instance)


class ClearWishlistView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        customer = self.request.user.customer
        return customer.wishlist

    def perform_destroy(self, instance):
        # instance here is the wishlist
        instance.clear()


class GetWishlistView(generics.ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        return customer.wishlist


class CartItemListCreateDeleteView(generics.ListCreateAPIView):
    serializer_class = CartItemListCreateSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = self.request.user
        items = CartItem.objects.filter(customer__user=customer).prefetch_related(
            "product"
        )
        return items

    def delete(self, request, *args, **kwargs):
        customer = self.request.user.customer
        cart_items = CartItem.objects.filter(customer=customer)
        cart_items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemDeleteUpdateView(DestroyModelMixin, generics.UpdateAPIView):
    serializer_class = CartItemUpdateDeleteSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = self.request.user
        items = CartItem.objects.filter(customer__user=customer)
        return items

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
