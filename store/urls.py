from django.urls import path

from .views import CategoriesListView, ProductView

urlpatterns = [
    path("categories/", CategoriesListView.as_view(), name="categories_view"),
    path("products/", ProductView.as_view(), name="products_view"),
    path("products/<int:pk>", ProductView.as_view(), name="products_view"),
]
