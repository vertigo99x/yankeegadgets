from django.contrib import admin

from .models import Category, Products, AdBanner, WishList, CartList, Customers

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(AdBanner)
admin.site.register(WishList)
admin.site.register(CartList)
admin.site.register(Customers)
