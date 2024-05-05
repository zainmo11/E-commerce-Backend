from django.db import models


# Create your models here.
class Order(models.Model):
    state_types = {"p": "pending", "o": "out for delivery", "d": "delivered"}

    payment_set = models.ForeignKey(
        to="PaymentDetails", on_delete=models.DO_NOTHING, null=True
    )
    amount = models.IntegerField()
    state = models.CharField(choices=state_types, max_length=1)
    customer = models.ForeignKey(
        "stats.customer", on_delete=models.DO_NOTHING, null=True
    )
    products = models.ManyToManyField(to="store.product", through="OrderItems")

    def __str__(self):
        return self.customer.user.username + "'s order ID " + self.id


class PaymentDetails(models.Model):
    payment_method = models.CharField(max_length=50)
    credit_card_number = models.CharField(max_length=16)
    credit_card_expiry = models.DateField()
    payment_date = models.DateTimeField()
    payment_amount = models.IntegerField()

    def __str__(self):
        return (
            "payment method :"
            + self.payment_method
            + " payment of :"
            + str(self.payment_amount)
            + " made on :"
            + str(self.payment_date)
            + " with card number "
            + self.credit_card_number
        )


class OrderItems(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey("store.product", on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

    def __str__(self):
        return (
            "order ID: "
            + self.order.id
            + ", item: "
            + self.product.name
            + ", qty: "
            + self.quantity
        )
