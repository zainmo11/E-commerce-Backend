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


class ProductView(RetrieveModelMixin, ListModelMixin, generics.CreateAPIView):
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

    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request)
        except AssertionError:
            pass

        return self.list(request)
