from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unisex', 'Unisex'),
    )

    CATEGORY_CHOICES = (
        ('Haircare', 'Haircare'),
        ('Skincare', 'Skincare'),
        ('Bodycare', 'Bodycare'),
        ('Fragrance', 'Fragrance'),
        ('Beauty Boxes', 'Beauty Boxes'),
        ('Other', "Other"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Other')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Unisex")
    quantity = models.IntegerField(default=1)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', blank=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class ShippingDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Shipping Details for {self.user.username}"

class Article(models.Model):
    CATEGORY_CHOICES = (
        ('Haircare', 'Haircare'),
        ('Skincare', 'Skincare'),
        ('Bodycare', 'Bodycare'),
        ('Fragrance', 'Fragrance'),
    )

    title = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='article_images/')
    main_content = models.TextField()
    secondary_image = models.ImageField(upload_to='article_images/', null=True, blank=True)
    secondary_content = models.TextField(default='')
    publication_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Haircare')

    def __str__(self):
        return self.title