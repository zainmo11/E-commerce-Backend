from django_filters import BaseInFilter, NumberFilter
from django_filters.rest_framework import FilterSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Product


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ProductFilter(FilterSet):
    categories = NumberInFilter(field_name="category", lookup_expr="in")
    price = NumberInFilter(field_name="price", method="filter_price")

    rating = NumberFilter(field_name="stats__rating", lookup_expr="gte")

    class Meta:
        model = Product
        fields = ["categories", "rating"]

    def filter_price(self, queryset, name, value):
        if len(value) == 2:
            lookups = {f"{name}__gte": min(value), f"{name}__lte": max(value)}
            return queryset.filter(**lookups)

        return queryset.filter(**{f"{name}__lte": value[0]})


class PlainPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        return Response(data)

    def get_paginated_response_schema(self, schema):
        return schema
