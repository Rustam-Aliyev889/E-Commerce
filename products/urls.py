from django.urls import path
from .views import (product_list, product_detail, create_product,get_cart_count,
         add_to_cart, view_cart, remove_from_cart, article_list, order_summary)




urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('articles/', article_list, name='article_list'),
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('create/', create_product, name='create_product'),
    path('cart/', view_cart, name='view_cart'),
    path('get-cart-count/', get_cart_count, name='get_cart_count'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('order-summary/', order_summary, name='order_summary'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
]