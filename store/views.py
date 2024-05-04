from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import SAFE_METHODS

from authentication.authenticator import JWTAuthenticator

from .filters import PlainPageNumberPagination, ProductFilter
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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]

    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    pagination_class = PlainPageNumberPagination

    search_fields = ["name", "description"]

    def get_queryset(self):
        seller = self.request.query_params.get("seller")
        if seller:
            return Product.objects.filter(seller=seller)

        return Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthenticator]
    permission_classes = [IsSellerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if self.request.method not in SAFE_METHODS:
            return Product.objects.filter(seller__user=user)

        return Product.objects.all()
