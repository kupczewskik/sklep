from django.contrib import admin
from django.contrib import admin
from .models import Product, Category, Order, OrderItem

# Rejestracja modeli w panelu administracyjnym
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
# Register your models here.
