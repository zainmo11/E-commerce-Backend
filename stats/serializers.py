from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Avg
from rest_framework import serializers

from authentication.serializers import UserSerializer
from paymentservice.serializers import OrderSerializer
from store.models import Product
from store.serializers import (
    PathField,
    PrivateProductSerializer,
    ProductSerializer,
)

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
    user = UserSerializer()
    order_set = OrderSerializer(read_only=True, many=True)

    class Meta:
        model = Customer
        fields = ["user", "avatar", "address", "wishlist", "order_set"]
        read_only_fields = ["wishlist"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user

        user.username = user_data.get("username", user.username)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)

        password = user_data.get("password", None)
        if password:
            user.set_password(password)
        user.save()

        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance


class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(source="product_set", read_only=True, many=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ["user", "company_name", "location", "products", "avatar"]

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

    def get_avatar(self, obj):
        customer = obj.user.customer
        return customer.avatar


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


class CartListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        total_price = sum(
            cart_item.product.price * cart_item.quantity for cart_item in data
        )
        serialized_data = super().to_representation(data)
        new_data = {"cart": serialized_data, "total_price": total_price}
        return new_data

    @property
    def data(self):
        """
        The same implementation of BaseSerializer to skip the implementation
        of ListSerializer
        """

        if not hasattr(self, "_data"):
            if self.instance is not None and not getattr(self, "_errors", None):
                self._data = self.to_representation(self.instance)
            elif hasattr(self, "_validated_data") and not getattr(
                self, "_errors", None
            ):
                self._data = self.to_representation(self.validated_data)
            else:
                self._data = self.get_initial()
        return self._data


class CartItemListCreateSerializer(serializers.ModelSerializer):
    product = PathField(
        view_name="store:products_retrieve", queryset=Product.objects.all()
    )
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "customer", "product", "quantity", "product_details"]
        read_only_fields = ["id", "customer"]
        validators = [validate_quantity]

        list_serializer_class = CartListSerializer

    def create(self, validated_data):
        try:
            validated_data["customer"] = self.context["request"].user.customer
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"details": "The customer already has this product in his cart"}
            )

    def get_product_details(self, obj):
        return ProductSerializer(obj.product).data


class CartItemUpdateDeleteSerializer(serializers.ModelSerializer):
    product = PathField(view_name="store:products_retrieve", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "customer", "product", "quantity"]
        read_only_fields = ["id", "customer", "product"]
        validators = [validate_quantity]
