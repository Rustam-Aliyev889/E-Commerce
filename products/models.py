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

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', blank=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
