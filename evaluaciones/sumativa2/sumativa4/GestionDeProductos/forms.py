# GestionDeProductos/forms.py
from django import forms
from .models import Producto, ProductoCaracteristica

class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio', 'categoria', 'marca']

class ProductFeatureForm(forms.ModelForm):
    class Meta:
        model = ProductoCaracteristica
        fields = ['caracteristica', 'valor']

