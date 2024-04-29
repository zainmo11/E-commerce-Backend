from django.urls import path

from .views import CategoriesListView, ProductDetailView, ProductListView

urlpatterns = [
    path("categories/", CategoriesListView.as_view(), name="categories_view"),
    path("products/", ProductListView.as_view(), name="products_view"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="products_view"),
]
