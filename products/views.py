from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Product, Cart, Order, Article,ShippingDetails
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import ProductForm, CartAddProductForm, SignUpForm, ShippingDetailsForm
import random
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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

def register(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, f" Thank you for registering {username}. You are now now loggged in.")
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'registration/register.html', {'form':form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login_user')  # Must match URL pattern name
    else:
        return render(request, 'registration/login.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

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
def shipping_details(request):
    existing_shipping_details = ShippingDetails.objects.filter(user=request.user).first()

    if existing_shipping_details:
        # If shipping details already exist for the user, -> redirect or display a message(4 later)
        messages.warning(request, 'Shipping details already exist.')
        return redirect('checkout')  

    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST)
        if form.is_valid():
            shipping_details = form.save(commit=False)
            shipping_details.user = request.user
            shipping_details.save()
            messages.success(request, 'Shipping details added successfully.')
            return redirect('checkout')
    else:
        form = ShippingDetailsForm()

    return render(request, 'products/shipping_details.html', {'form': form})

def edit_shipping_details(request):
    shipping_details, created = ShippingDetails.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST, instance=shipping_details)
        if form.is_valid():
            form.save()
            messages.success(request, "Your shipping details have been updated.")
            return redirect('checkout')
    else:
        form = ShippingDetailsForm(instance=shipping_details)

    return render(request, 'products/edit_shipping_details.html', {'form': form})

def order_summary(request):
    order = Order.objects.get(user=request.user, ordered=False)
    return render(request, 'order_summary.html', {'order': order})

@login_required
def checkout(request):
    # Cart details
    cart, created = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    for product in products:
        product.total_price = product.price * product.quantity

    # Calculate the overall total price
    total_price = sum(product.total_price for product in products)

    # Shipping details
    try:
        shipping_details = ShippingDetails.objects.get(user=request.user)
    except ShippingDetails.DoesNotExist:
        shipping_details = None

    # Stripe public key in the context
    context = {
        'cart': cart,
        'products': products,
        'total_price': total_price,
        'shipping_details': shipping_details,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    intent = None

    if request.method == 'POST':
        # Get the Stripe token from the form data
        token = request.POST.get('stripeToken')

        if not token or not token.startswith('tok_'):
            # The token is invalid or missing
            messages.error(request, 'Invalid or missing Stripe token.')
            return render(request, 'products/checkout.html', context)

        try:
            # Check if a customer with the email already exists
            customer = stripe.Customer.list(email=request.user.email, limit=1).data
            if customer:
                customer = customer[0]
            else:
                # Create a new customer in Stripe
                customer = stripe.Customer.create(
                    email=request.user.email,
                    source=token,
                )

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),
                currency='usd',
                description='Order',
                customer=customer.id,
            )

        except stripe.error.CardError as e:
            # The card has been declined
            messages.error(request, f"Payment failed: {e.error.message}")

        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            messages.error(request, f"Stripe error: {str(e)}")

        except Exception as e:
            # Handle other exceptions
            messages.error(request, f"Error processing payment: {str(e)}")

    context['client_secret'] = intent.client_secret if intent else None
    return render(request, 'products/checkout.html', context)

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

