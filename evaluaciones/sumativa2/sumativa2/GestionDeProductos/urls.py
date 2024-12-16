# GestionDeProductos/urls.py
from django.urls import path
from . import views
from .api import api

urlpatterns = [
    path('', views.login_view, name='login'),
    path('productos/', views.index, name='index'),
    path('productos/registrar/', views.producto_create, name='registro'),
    path('productos/editar/<int:pk>/', views.producto_edit, name='producto_edit'),
    path('productos/eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),
    path('productos/resultado/<int:pk>/', views.result, name='result'),
    path('api/', api.urls),  # Add this line to include the API routes
    path('view-session-data/', views.view_session_data, name='view_session_data')
]