from rest_framework import serializers

from stats.models import CartItem
from store.serializers import ProductSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["payment_method", "amount", "state", "customer", "products"]
        read_only_fields = ["amount", "state", "customer", "products"]

    def create(self, validated_data):
        customer = self.context["customer"]
        user_cart = CartItem.objects.filter(customer=customer).select_related("product")
        order = Order.objects.create(**validated_data, customer=customer, amount=0)

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
        order.save()

        return order
