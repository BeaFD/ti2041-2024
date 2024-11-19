# GestionDeProductos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Producto, ProductoCaracteristica, Caracteristica, Marca, Categoria
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['login_date'] = str(timezone.now())
            request.session['role'] = 'ADMIN_PRODUCTS' if user.groups.filter(name='ADMIN_PRODUCTS').exists() else 'USER'
            return redirect('/productos')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'GestionDeProductos/login.html')

@login_required
@permission_required('GestionDeProductos.add_producto', raise_exception=True)
def producto_create(request):
    if request.method == 'POST':
        registro = ProductForm(request.POST)
        if registro.is_valid():
            producto = registro.save()
            caracteristicas = request.POST.getlist('caracteristica')
            valores = request.POST.getlist('valor')
            for caracteristica, valor in zip(caracteristicas, valores):
                ProductoCaracteristica.objects.create(producto=producto, caracteristica_id=caracteristica, valor=valor)
            return redirect('result', pk=producto.pk)
    else:
        registro = ProductForm()
        caracteristicas = Caracteristica.objects.all()
    return render(request, 'GestionDeProductos/registro.html', {'registro': registro, 'caracteristicas': caracteristicas})

@login_required
def index(request):
    productos = Producto.objects.all().prefetch_related('caracteristica', 'categoria', 'marca')

    search_query = request.GET.get('search')
    filter_type = request.GET.get('filter_type')

    if search_query and filter_type:
        if filter_type == 'marca':
            productos = productos.filter(marca__name__icontains=search_query)
        elif filter_type == 'categoria':
            productos = productos.filter(categoria__name__icontains=search_query)
        elif filter_type == 'nombre':
            productos = productos.filter(nombre__icontains=search_query)
        elif filter_type == 'codigo':
            productos = productos.filter(codigo__icontains=search_query)
        else:
            # Handle specific characteristics
            productos = productos.filter(productocaracteristica__caracteristica__name__icontains=filter_type, productocaracteristica__valor__icontains=search_query)

    return render(request, 'GestionDeProductos/index.html', {
        'productos': productos,
        'marcas': Marca.objects.all(),
        'categorias': Categoria.objects.all(),
        'caracteristicas': Caracteristica.objects.all(),
    })

@login_required
@permission_required('GestionDeProductos.change_producto', raise_exception=True)
def producto_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        registro = ProductForm(request.POST, instance=producto)
        if registro.is_valid():
            producto = registro.save()
            ProductoCaracteristica.objects.filter(producto=producto).delete()
            caracteristicas = request.POST.getlist('caracteristica')
            valores = request.POST.getlist('valor')
            for caracteristica, valor in zip(caracteristicas, valores):
                ProductoCaracteristica.objects.create(producto=producto, caracteristica_id=caracteristica, valor=valor)
            return redirect('result', pk=producto.pk)
    else:
        registro = ProductForm(instance=producto)
        caracteristicas = Caracteristica.objects.all()
        producto_caracteristicas = ProductoCaracteristica.objects.filter(producto=producto)
    return render(request, 'GestionDeProductos/registro.html', {
        'registro': registro,
        'caracteristicas': caracteristicas,
        'producto_caracteristicas': producto_caracteristicas
    })

@login_required
@permission_required('GestionDeProductos.delete_producto', raise_exception=True)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('index')
    return render(request, {'producto': producto})

@login_required
@permission_required('GestionDeProductos.view_producto', raise_exception=True)
def result(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'GestionDeProductos/result.html', {'producto': producto})