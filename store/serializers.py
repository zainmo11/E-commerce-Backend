from rest_framework import serializers

from .models import Category, Product


class ProductSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    example_products = serializers.SerializerMethodField("get_example_products")
    products_number = serializers.IntegerField(source="products_num")

    class Meta:
        model = Category
        fields = ["id", "name", "products_number", "example_products"]
        read_only_fields = ["id", "products_number", "example_products"]

    def get_example_products(self, obj):
        example_products = obj.product_set.all()[: self.context["n_products"]]
        serialized_data = ProductSerlializer(example_products, many=True)
        return serialized_data.data
