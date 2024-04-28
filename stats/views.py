from rest_framework import generics

from .models import Seller
from .serializers import SellerSerializer


class SellerListView(generics.ListAPIView):
    serializer_class = SellerSerializer

    def get_queryset(self):
        number = int(self.request.query_params.get("n", 10))
        queryset = Seller.objects.all()[:number]
        return queryset
