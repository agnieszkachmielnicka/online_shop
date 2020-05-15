from django.contrib import admin

from .models import Product, Category, Basket, ProductsList, ProductsInBasket, Country, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Basket)
admin.site.register(ProductsList)
admin.site.register(ProductsInBasket)
admin.site.register(Country)
admin.site.register(Order)
