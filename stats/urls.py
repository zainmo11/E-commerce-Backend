from django.urls import path

from stats.views import (
    CartItemDeleteUpdateView,
    CartItemListDeleteView,
    SellerListView,
)

urlpatterns = [
    path("sellers/", SellerListView.as_view()),
    path("cart/", CartItemListDeleteView.as_view()),
    path("cart-items/", CartItemListDeleteView.as_view()),
    path("cart-items/<int:pk>", CartItemDeleteUpdateView.as_view()),
]
