from datetime import datetime

import pytz
from rest_framework import serializers

from paymentservice.models import PaymentDetails
from stats.models import CartItem
from store.serializers import ProductSerializer

from .models import Order


class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = "__all__"
        read_only_fields = ["id", "payment_amount"]

    def validate(self, attrs):
        payment_date = datetime.fromisoformat("2024-05-04T20:10:34.147Z").replace(
            tzinfo=pytz.utc
        )
        if attrs["payment_method"] not in ["credit card", "cash"]:
            raise serializers.ValidationError("Invalid payment method")

        if attrs["payment_method"] == "credit card":
            if len(attrs["credit_card_number"]) != 16:
                raise serializers.ValidationError("Invalid credit card number")

            if attrs["payment_amount"] < 0:
                raise serializers.ValidationError("Invalid payment amount")

            if attrs["payment_date"] > payment_date:
                raise serializers.ValidationError("Invalid payment date")

            if attrs["credit_card_expiry"] < datetime.date(datetime.now()):
                raise serializers.ValidationError("Invalid credit card expiry date")

        if attrs["payment_method"] == "cash":
            if len(attrs["payment_amount"]) < 0:
                raise serializers.ValidationError("Invalid payment amount")
            if attrs["payment_date"] > payment_date:
                raise serializers.ValidationError("Invalid payment date")

        return attrs


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    payment_set = PaymentDetailsSerializer()

    class Meta:
        model = Order
        fields = [
            "payment_set",
            "amount",
            "state",
            "customer",
            "products",
        ]
        read_only_fields = ["amount", "state", "customer", "products"]

    def create(self, validated_data):
        customer = self.context["customer"]
        user_cart = CartItem.objects.filter(customer=customer).select_related("product")
        order = Order.objects.create(customer=customer, amount=0)
        payment_details = validated_data.pop("payment_set")
        # this whole operation could be optimized
        amount = 0
        for cart_item in user_cart:
            referred_product = cart_item.product
            product_seller = referred_product.seller

            referred_product.quantity -= cart_item.quantity
            referred_product.total_sold += cart_item.quantity
            product_seller.total_products_sold += cart_item.quantity
            product_seller.total_revenue += referred_product.price
            amount += referred_product.price

            order.products.add(
                referred_product, through_defaults={"quantity": cart_item.quantity}
            )

            # the two saves here could be optimized by appending the different
            # sellers to a set and the different products and saving them invidually
            product_seller.save()
            referred_product.save()

        order.amount = amount
        payment_details["payment_amount"] = amount
        order.payment_set = PaymentDetails.objects.create(**payment_details)
        order.save()

        return order
