from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Goods,Product

class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'