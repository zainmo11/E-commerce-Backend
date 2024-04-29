from django.contrib import admin

from .models import CartItem, Customer, Seller

admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(CartItem)
