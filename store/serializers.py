from urllib.parse import urlencode

from django.db import models
from django.urls import reverse
from rest_framework import serializers

from .models import Category, Product


class PathField(serializers.PrimaryKeyRelatedField):
    def __init__(self, *args, **kwargs):
        self.view_name = kwargs.pop("view_name")
        self.query_param_name = kwargs.pop("query_param_name", None)
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if self.query_param_name:
            query_param_dict = {self.query_param_name: value}
            return reverse(self.view_name) + "?" + urlencode(query_param_dict)
        return reverse(self.view_name, args=[value])


class ProductSerializer(serializers.ModelSerializer):
    product_path = PathField(
        view_name="store:products_retrieve", source="id", read_only=True
    )
    category_name = serializers.CharField(source="category.name", read_only=True)
    seller_name = serializers.CharField(source="seller.company_name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "specs",
            "category",
            "category_name",
            "seller",
            "seller_name",
            "product_path",
        ]
        read_only_fields = ["id", "seller"]

    def create(self, validated_data):
        validated_data["seller"] = self.context["request"].user.seller
        return super().create(validated_data)


class PrivateProductSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ["total_sold"]


class CategorySerializer(serializers.ModelSerializer):
    example_products = serializers.SerializerMethodField("get_example_products")
    products_number = serializers.IntegerField(source="products_num")
    category_path = PathField(
        source="id",
        view_name="store:products_view",
        query_param_name="cat",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "thumbnail",
            "name",
            "products_number",
            "example_products",
            "category_path",
        ]
        read_only_fields = [
            "id",
            "products_number",
            "example_products",
            "category_path",
        ]

    def get_example_products(self, obj):
        # pagination should be implemented here but no time :(
        example_products = obj.product_set.all()[: self.context["n_products"]]
        serialized_data = ProductSerializer(example_products, many=True)
        return serialized_data.data
