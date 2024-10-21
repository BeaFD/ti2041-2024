from django.shortcuts import render, redirect
from .models import Producto, Marca, Categoria, Caracteristica, ProductoCaracteristica

productos = []

def registro_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        marca_id = request.POST.get('marca')
        categoria_id = request.POST.get('categoria')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        caracteristica_id = request.POST.get('caracteristica')
        valor_caracteristica = request.POST.get('valor_caracteristica')

        if codigo and nombre and marca_id:
            try:
                marca = Marca.objects.get(id=marca_id)
                categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
                
                # Crear el producto
                producto = Producto.objects.create(
                    codigo=codigo,
                    nombre=nombre,
                    marca=marca,
                    categoria=categoria,
                    fecha_vencimiento=fecha_vencimiento
                )
                
                # Agregar la característica si se proporciona
                if caracteristica_id and valor_caracteristica:
                    caracteristica = Caracteristica.objects.get(id=caracteristica_id)
                    ProductoCaracteristica.objects.create(
                        producto=producto,
                        caracteristica=caracteristica,
                        valor=valor_caracteristica
                    )
                
                return redirect('consulta')
            except Exception as e:
                error = f"Error al registrar el producto: {str(e)}"
                return render(request, 'registro.html', {
                    'error': error,
                    'marcas': Marca.objects.all(),
                    'categorias': Categoria.objects.all(),
                    'caracteristicas': Caracteristica.objects.all(),
                })

        else:
            error = "Los campos de código, nombre y marca son obligatorios."
            return render(request, 'registro.html', {
                'error': error,
                'marcas': Marca.objects.all(),
                'categorias': Categoria.objects.all(),
                'caracteristicas': Caracteristica.objects.all(),
            })
    else:
        return render(request, 'registro.html', {
            'marcas': Marca.objects.all(),
            'categorias': Categoria.objects.all(),
            'caracteristicas': Caracteristica.objects.all(),
        })

def resultado_producto(request):
    if productos:
        ultimo_producto = productos[-1]
    else:
        ultimo_producto = None

    return render(request, 'resultado.html', {'producto': ultimo_producto})


def consulta_productos(request):
    # Obtener los filtros del request
    marca_id = request.GET.get('marca')
    categoria_id = request.GET.get('categoria')
    nombre = request.GET.get('nombre')
    caracteristica_id = request.GET.get('caracteristica')

    # Filtrar los productos según los parámetros proporcionados
    productos = Producto.objects.all()
    if marca_id:
        productos = productos.filter(marca_id=marca_id)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if caracteristica_id:
        productos = productos.filter(caracteristicas__id=caracteristica_id)

    # Obtener todas las marcas, categorías y características para los filtros
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = Caracteristica.objects.all()

    context = {
        'productos': productos,
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas,
    }
    return render(request, 'consulta.html', context)