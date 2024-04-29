from rest_framework import generics
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from authentication.authenticator import JWTAuthenticator

from .models import Category, Product
from .permissions import IsSellerOrReadOnly
from .serializers import CategorySerializer, ProductSerlializer


class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["n_products"] = int(self.request.query_params.get("products", 0))
        return context


class ProductListView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsSellerOrReadOnly]
    serializer_class = ProductSerlializer

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


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerlializer
    queryset = Product.objects.all()
