from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order, Article
from .forms import ProductForm
from .forms import CartAddProductForm
import random
from django.http import JsonResponse

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
    total_price = sum(product.price * product.quantity for product in products)

    return render(request, 'products/cart.html', {'cart': cart, 'products': products, 'total_price': total_price})
    #return render(request, 'products/cart.html', {'cart': cart, 'products': products})

def get_cart_count(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        item_count = cart.products.count()
    else:
        # anonymous user's cart count (if applicable)
        item_count = 0  # logic for anonymous users

    return JsonResponse({'item_count': item_count})

def add_to_cart(request, product_id):
    try:
        product_id = int(product_id)
    except ValueError:
        pass

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Gets the quantity from the AJAX request data
    quantity = int(request.POST.get('quantity', 1))

        #To update the quantity in the Product model
    product.quantity += quantity
    product.save()
    cart.products.add(product)

    response_data = {'product_name': product.name, 'success': True,'quantity': product.quantity }

    return JsonResponse(response_data)


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    product.quantity = 0
    product.save()
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
            new_quantity = cart_product_form.cleaned_data['quantity']
            # Updates for product quantity 
            product.quantity = new_quantity
            product.save()

            return redirect('view_cart')
        else:
            # If the form is not valid, will render the product detail page with errors
            return render(request, 'products/product_detail.html', {'product': product, 'cart_product_form': cart_product_form, 'product_id': product_id})
    
    # If the request method is not POST, just renders the product detail page
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
