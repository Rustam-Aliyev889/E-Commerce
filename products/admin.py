from django.contrib import admin
from .models import Product, Article, ShippingDetails, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'user')
    search_fields = ('name', 'description', 'user__username')  # Allows searching by name, description, and user
    admin.site.register(Article)
    admin.site.register(ShippingDetails)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price')
    search_fields = ('user__username',)