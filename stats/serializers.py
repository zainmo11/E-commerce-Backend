from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Avg
from rest_framework import serializers

from authentication.serializers import UserSerializer
from store.models import Product
from store.serializers import PrivateProductSerializer, ProductSerializer

from .models import CartItem, Customer, Seller, Stats

User = get_user_model()


def validate_quantity(obj):
    if obj["quantity"] <= 0:
        raise serializers.ValidationError(
            {"details": "Product quantity must be greater than 0"}
        )
    return obj


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ["user", "avatar", "address", "wishlist"]
        read_only_fields = ["wishlist"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class CustomerReadUpdateDeleteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ["user", "avatar", "address", "wishlist"]
        read_only_fields = ["wishlist"]


class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(source="product_set", read_only=True, many=True)

    class Meta:
        model = Seller
        fields = ["user", "company_name", "location", "products"]

    def validate(self, data):
        self.user = self.context["request"].user
        try:
            Seller.objects.get(user=self.user)
            raise serializers.ValidationError({"details": "User is already a seller"})
        except ObjectDoesNotExist:
            pass
        return data

    def create(self, validated_data):
        return Seller.objects.create(
            user=self.user,
            company_name=validated_data["company_name"],
            location=validated_data["location"],
        )


class PrivateSellerSerializer(SellerSerializer):
    average_product_rating = serializers.SerializerMethodField("get_average_rating")
    products = PrivateProductSerializer(source="product_set", read_only=True, many=True)

    class Meta(SellerSerializer.Meta):
        fields = SellerSerializer.Meta.fields + [
            "total_revenue",
            "total_products_sold",
            "products_num",
            "out_of_stock_num",
            "average_product_rating",
        ]

    def get_average_rating(self, obj):
        return Stats.objects.filter(product__seller=obj).aggregate(
            Avg("rating", default=0)
        )["rating__avg"]


class WishlistProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )

    def create(self, validated_data):
        product = validated_data["product"]
        customer = self.context["request"].user.customer
        customer.wishlist.add(product)
        return product


class CartItemListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "customer", "product", "quantity"]
        read_only_fields = ["id", "customer"]
        validators = [validate_quantity]

    def create(self, validated_data):
        try:
            validated_data["customer"] = self.context["request"].user.customer
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"details": "The customer already has this product in his cart"}
            )


class CartItemUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "customer", "product", "quantity"]
        read_only_fields = ["id", "customer", "product"]
        validators = [validate_quantity]
