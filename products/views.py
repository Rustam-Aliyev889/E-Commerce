from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order
from .forms import ProductForm
from .forms import CartAddProductForm

def home(request):
    return render(request, 'base.html')

@login_required
def order_summary(request):
    order = Order.objects.get(user=request.user, ordered=False)
    return render(request, 'order_summary.html', {'order': order})

@login_required
def checkout(request):
    order = Order.objects.get(user=request.user, ordered=False)

    if request.method == 'POST':
        order.ordered = True
        order.save()
        return render(request, 'checkout.html', {'order': order})

    return render(request, 'checkout.html', {'order': order})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect('cart')

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    return render(request, 'cart/cart.html', {'cart': cart, 'products': products})

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.remove(product)
    return redirect('cart')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_product_form = CartAddProductForm()
    return render(request, 'products/product_detail.html', {'product': product, 'cart_product_form': cart_product_form})

#@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/create_product.html', {'form': form})
