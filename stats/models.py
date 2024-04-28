from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    wishlist = models.ManyToManyField(to="store.product")

    def __str__(self):
        return "Customer: " + self.user.username


class Seller(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    location = models.CharField(max_length=150)

    def __str__(self):
        return "Seller: " + self.company_name


class CartItem(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=True)
    cart_item = models.ForeignKey(
        to="store.product", on_delete=models.CASCADE, null=True
    )
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username + "'s cart"


class Stats(models.Model):
    product = models.OneToOneField(
        to="store.product", primary_key=True, on_delete=models.CASCADE
    )
    views = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return "Product: " + self.product.name + ", rating: " + self.rating


class Comment(models.Model):
    stats = models.ForeignKey(to=Stats, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    title = models.CharField(max_length=150, null=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
