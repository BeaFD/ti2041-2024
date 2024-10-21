# GestionDeProductos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.index, name='index'),
    path('productos/registrar/', views.producto_create, name='registro'),
    path('productos/editar/<int:pk>/', views.producto_edit, name='producto_edit'),
    path('productos/eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),
    path('productos/resultado/<int:pk>/', views.result, name='result'),
]