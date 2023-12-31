from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['user', 'name', 'description', 'price', 'image', 'category', 'gender', 'quantity']



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)