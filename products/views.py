from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order, Article
from .forms import ProductForm
from .forms import CartAddProductForm
import random

def home(request):
    beauty_boxes = Product.objects.filter(category='Beauty Boxes')

    # to shuffle the beauty boxes to display in random order
    beauty_boxes_shuffled = list(beauty_boxes)
    random.shuffle(beauty_boxes_shuffled)

    # to check for the gender filter
    gender_filter = request.GET.get('gender')

    # To apply additional filtering based on gender
    if gender_filter == 'male':
        beauty_boxes = [product for product in beauty_boxes_shuffled if product.gender == 'Male']
    elif gender_filter == 'female':
        beauty_boxes = [product for product in beauty_boxes_shuffled if product.gender == 'Female']
    else:
        beauty_boxes = beauty_boxes_shuffled

    return render(request, 'base.html', {'beauty_boxes': beauty_boxes})

def article_list(request):
    articles = Article.objects.all()

    # Gets the selected category from the query parameters
    category_filter = request.GET.get('category')

    # additional filtering based on the selected category
    if category_filter:
        articles = articles.filter(category=category_filter)
    else:
        # If no category is selected, shuffle articles and display only one random category
        random_category = random.choice(Article.CATEGORY_CHOICES)[0]
        articles = articles.filter(category=random_category)

    return render(request, 'articles/article_list.html', {'articles': articles, 'selected_category': category_filter})

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

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    return render(request, 'products/cart.html', {'cart': cart, 'products': products})

def add_to_cart(request, product_id):
    try:
        product_id = int(product_id)
    except ValueError:
        pass

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    
    beauty_boxes = Product.objects.filter(category='Beauty Boxes')

    return render(request, 'base.html', {'beauty_boxes': beauty_boxes})


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.remove(product)
    return redirect('view_cart')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_product_form = CartAddProductForm()

    if request.method == 'POST':
        cart_product_form = CartAddProductForm(request.POST)
        if cart_product_form.is_valid():
            # Handle adding product to the cart
            # You may need to modify this part based on your implementation
            # For example, you can use the Cart model to store the added products
            # and the session to keep track of the current user's cart
            # Add the logic to handle adding the product to the cart
            # After that, you can redirect the user to the cart view

            return redirect('view_cart')
        
        return render(request, 'products/product_detail.html', {'product': product, 'cart_product_form': cart_product_form, 'product_id': product_id})

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
