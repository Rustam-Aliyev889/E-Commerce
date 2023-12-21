from django.urls import path
from .views import product_list, product_detail, create_product, add_to_cart, view_cart, remove_from_cart


urlpatterns = [
    path('list/', product_list, name='product_list'),  # Adjust the URL pattern as needed
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('create/', create_product, name='create_product'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
]