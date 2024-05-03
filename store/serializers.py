from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import serializers

from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
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
            "seller",
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
    category_path = serializers.SerializerMethodField()

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
        example_products = obj.product_set.all()[: self.context["n_products"]]
        serialized_data = ProductSerializer(example_products, many=True)
        return serialized_data.data

    def get_category_path(self, obj):
        category_query_params = {"cat": obj.id}
        return reverse("store:products_view") + "?" + urlencode(category_query_params)
