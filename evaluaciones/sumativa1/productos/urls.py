from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_producto, name='registro'),
    path('resultado/', views.resultado_producto, name='resultado'),
    path('consulta/', views.consulta_productos, name='consulta'),
]
