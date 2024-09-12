from django.shortcuts import render, redirect

# Lista para almacenar los productos
productos = []

def registro_producto(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        # Validar que todos los campos estén completos
        if codigo and nombre and marca and fecha_vencimiento:
            producto = {
                'codigo': codigo,
                'nombre': nombre,
                'marca': marca,
                'fecha_vencimiento': fecha_vencimiento
            }
            productos.append(producto)  # Agregar el producto a la lista en memoria
            return redirect('resultado')  # Redirigir a la página de resultado tras el registro
        else:
            # Si hay campos faltantes, mostrar un mensaje de error
            error = "Todos los campos son obligatorios."
            return render(request, 'productos/registro.html', {'error': error})

    # Si es un GET (primera vez que se carga el formulario), mostrar el formulario vacío
    return render(request, 'productos/registro.html')

def resultado_producto(request):
    # Verificar si hay productos registrados
    if productos:
        ultimo_producto = productos[-1]  # Obtener el último producto de la lista
    else:
        ultimo_producto = None  # En caso de que no haya productos

    # Pasar el último producto a la plantilla
    return render(request, 'productos/resultado.html', {'producto': ultimo_producto})


def consulta_productos(request):
    return render(request, 'productos/consulta.html', {'productos': productos})
