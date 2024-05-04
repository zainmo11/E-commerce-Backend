from django.contrib import admin

from .models import CartItem, Customer, Seller, Stats

# Register your models here.
admin.site.register(Seller)
admin.site.register(Stats)
admin.site.register(Customer)
admin.site.register(CartItem)
