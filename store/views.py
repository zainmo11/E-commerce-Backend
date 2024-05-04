from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS

from authentication.authenticator import JWTAuthenticator

from .models import Category, Product
from .permissions import IsSellerOrReadOnly
from .serializers import CategorySerializer, ProductSerializer


class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related("product_set").all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["n_products"] = int(self.request.query_params.get("products", 10))
        return context


class ProductListView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsSellerOrReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):
        seller = self.request.query_params.get("seller")
        if seller:
            return Product.objects.filter(seller=seller)

        return Product.objects.all()

    def filter_queryset(self, queryset):
        # May use django filters later
        # TODO: add all other filter, best sellers
        filter = self.request.query_params.get("filter", "")
        if filter == "hottest":
            return queryset.order_by("price")

        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsSellerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if self.request.method not in SAFE_METHODS:
            return Product.objects.filter(seller__user=user)

        return Product.objects.all()
