from django.contrib import admin

from .models import CartItem, Customer, Seller

# Register your models here.
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(CartItem)
