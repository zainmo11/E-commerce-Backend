from django.urls import path

from .views import (
    AddProductToWishlistView,
    CartItemDeleteUpdateView,
    CartItemListCreateDeleteView,
    ClearWishlistView,
    GetWishlistView,
    LowOnStockProductsView,
    PrivateSellerInfoView,
    RemoveProductWishlistView,
    SellerListView,
)

urlpatterns = [
    path("sellers/", SellerListView.as_view()),
    path("my-seller-info/", PrivateSellerInfoView.as_view()),
    path("low-stock-products/", LowOnStockProductsView.as_view()),
    path("cart-items/", CartItemListCreateDeleteView.as_view()),
    path("cart-items/<int:pk>", CartItemDeleteUpdateView.as_view()),
    path("wishlist-product/", AddProductToWishlistView.as_view()),
    path("remove-product/<int:pk>/", RemoveProductWishlistView.as_view()),
    path("clear-wishlist/", ClearWishlistView.as_view()),
    path("get-wishlist/", GetWishlistView.as_view(), name="get_wishlist"),
]
