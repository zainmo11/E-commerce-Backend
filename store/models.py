from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    thumbnail = models.CharField(max_length=250)
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    specs = models.JSONField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(to="stats.seller", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    link = models.CharField(max_length=250)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    color = models.ForeignKey(to=Color, on_delete=models.CASCADE, null=True)
