from rest_framework import serializers

from stats.models import CartItem
from store.serializers import ProductSerlializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerlializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["payment_method", "amount", "state", "customer", "products"]
        read_only_fields = ["amount", "state", "customer", "products"]

    def create(self, validated_data):
        customer = self.context["customer"]
        user_cart = CartItem.objects.filter(customer=customer).select_related(
            "cart_item"
        )
        order = Order.objects.create(**validated_data, customer=customer, amount=0)

        # this whole operation could be optimized
        amount = 0
        for cart_item in user_cart:
            referred_product = cart_item.cart_item
            referred_product.quantity -= cart_item.quantity
            amount += referred_product.price
            order.products.add(
                referred_product, through_defaults={"quantity": cart_item.quantity}
            )
            referred_product.save()
        order.amount = amount
        order.save()

        return order
