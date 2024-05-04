from django.contrib.auth import get_user_model
from django.db import models

from store.models import Product

User = get_user_model()


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    avatar = models.URLField(max_length=400, blank=True)
    address = models.CharField(max_length=150, blank=True)
    wishlist = models.ManyToManyField(to="store.product", blank=True)

    def __str__(self):
        return "Customer: " + self.user.username


class Seller(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_products_sold = models.IntegerField(default=0)
    company_name = models.CharField(max_length=50)
    location = models.CharField(max_length=150)

    def __str__(self):
        return "Seller: " + self.company_name

    @property
    def products_num(self):
        return self.product_set.count()

    @property
    def out_of_stock_num(self):
        return self.product_set.filter(quantity=0).count()


class CartItem(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(to="store.product", on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "product"], name="user_cart_item_constraint"
            )
        ]

    def __str__(self):
        return self.customer.user.username + "'s cart"


class Stats(models.Model):
    product = models.OneToOneField(
        to="store.product", primary_key=True, on_delete=models.CASCADE
    )
    views = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return "Product: " + self.product.name + ", rating: " + str(self.rating)


class Comment(models.Model):
    stats = models.ForeignKey(to=Stats, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    title = models.CharField(max_length=150, null=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
