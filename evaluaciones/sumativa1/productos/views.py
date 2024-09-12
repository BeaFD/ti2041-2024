from django.shortcuts import render, redirect

productos = []

def registro_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        if codigo and nombre and marca and fecha_vencimiento:
            producto = {
                'codigo': codigo,
                'nombre': nombre,
                'marca': marca,
                'fecha_vencimiento': fecha_vencimiento
            }
            productos.append(producto)
            return redirect('resultado')
        else:
            error = "Todos los campos son obligatorios."
            return render(request, 'registro.html', {'error': error})
    return render(request, 'registro.html')

def resultado_producto(request):
    if productos:
        ultimo_producto = productos[-1]
    else:
        ultimo_producto = None

    return render(request, 'resultado.html', {'producto': ultimo_producto})


def consulta_productos(request):
    return render(request, 'consulta.html', {'productos': productos})
