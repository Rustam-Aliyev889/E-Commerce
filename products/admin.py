from django.contrib import admin
from .models import Product, Article

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'user')
    search_fields = ('name', 'description', 'user__username')  # Allows searching by name, description, and user
    admin.site.register(Article)
