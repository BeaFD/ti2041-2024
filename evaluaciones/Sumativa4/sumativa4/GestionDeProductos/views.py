import requests
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings

API_BASE_URL = 'http://localhost:8000/api'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        logger.info(f"Attempting to authenticate user: {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"User authenticated: {username}")
            # Obtain JWT token
            response = requests.post(f'{API_BASE_URL}/token/', json={'username': username, 'password': password})
            if response.status_code == 200:
                token = response.json().get('token')
                request.session['jwt_token'] = token
                request.session['username'] = user.username
                request.session['login_date'] = str(timezone.now())
                request.session['role'] = 'ADMIN_PRODUCTS' if user.groups.filter(name='ADMIN_PRODUCTS').exists() else 'USER'
                logger.info(f"JWT Token obtained and saved: {token}")
                return redirect('/productos')
            else:
                logger.error(f"Failed to obtain token: {response.status_code} {response.text}")
                return HttpResponse('Failed to obtain token')
        else:
            logger.error("Invalid login")
            return HttpResponse('Invalid login')
    return render(request, 'GestionDeProductos/login.html')

@login_required
@permission_required('GestionDeProductos.add_producto', raise_exception=True)
def producto_create(request):
    categorias = []
    caracteristicas = []
    marcas = []
    producto_caracteristicas = []

    if request.method == 'POST':
        data = {
            'codigo': request.POST['codigo'],
            'nombre': request.POST['nombre'],
            'precio': request.POST['precio'],
            'categoria': request.POST['categoria'],
            'marca': request.POST['marca'],
            'caracteristicas': []
        }
        caracteristicas = request.POST.getlist('caracteristica')
        valores = request.POST.getlist('valor')
        for caracteristica, valor in zip(caracteristicas, valores):
            if caracteristica:  # Ensure caracteristica is not empty
                data['caracteristicas'].append({'caracteristica_id': caracteristica, 'valor': valor})
        
        headers = {'Authorization': f'Bearer {request.session.get("jwt_token")}'}
        logger.info(f"Creating product with data: {data}")
        logger.info(f"Using JWT Token: {request.session.get('jwt_token')}")
        response = requests.post(f'{API_BASE_URL}/productos/', json=data, headers=headers)
        if response.status_code == 201:
            producto = response.json()
            producto_id = producto['codigo']
            logger.info(f"Product created with ID: {producto_id}")
            return redirect(f'/productos/resultado/{producto_id}/')
        else:
            logger.error(f"Failed to create product: {response.status_code} {response.text}")
            producto = {}
    else:
        caracteristicas_response = requests.get(f'{API_BASE_URL}/caracteristicas/')
        categorias_response = requests.get(f'{API_BASE_URL}/categorias/')
        marcas_response = requests.get(f'{API_BASE_URL}/marcas/')
        if caracteristicas_response.status_code == 200:
            caracteristicas = caracteristicas_response.json()
        if categorias_response.status_code == 200:
            categorias = categorias_response.json()
        if marcas_response.status_code == 200:
            marcas = marcas_response.json()

    return render(request, 'GestionDeProductos/registro.html', {
        'producto': {},
        'caracteristicas': caracteristicas,
        'categorias': categorias,
        'marcas': marcas,
        'producto_caracteristicas': producto_caracteristicas
    })

@login_required
def index(request):
    headers = {'Authorization': f'Bearer {request.session.get("jwt_token")}'}
    logger.info(f"Fetching products with JWT Token: {request.session.get('jwt_token')}")
    response = requests.get(f'{API_BASE_URL}/productos/', headers=headers)
    if response.status_code == 200:
        productos = response.json()
        logger.info(f"Products fetched successfully")
    else:
        productos = []
        logger.error(f"Failed to fetch products: {response.status_code} {response.text}")

    search_query = request.GET.get('search')
    filter_type = request.GET.get('filter_type')

    if search_query and filter_type:
        if filter_type == 'marca':
            productos = [p for p in productos if search_query.lower() in p['marca'].lower()]
        elif filter_type == 'categoria':
            productos = [p for p in productos if search_query.lower() in p['categoria'].lower()]
        elif filter_type == 'nombre':
            productos = [p for p in productos if search_query.lower() in p['nombre'].lower()]
        elif filter_type == 'codigo':
            productos = [p for p in productos if search_query.lower() in p['codigo'].lower()]
        else:
            # Handle specific characteristics
            productos = [p for p in productos if any(search_query.lower() in c['valor'].lower() for c in p['caracteristicas'])]

    marcas_response = requests.get(f'{API_BASE_URL}/marcas/', headers=headers)
    categorias_response = requests.get(f'{API_BASE_URL}/categorias/', headers=headers)
    caracteristicas_response = requests.get(f'{API_BASE_URL}/caracteristicas/', headers=headers)

    marcas = marcas_response.json() if marcas_response.status_code == 200 else []
    categorias = categorias_response.json() if categorias_response.status_code == 200 else []
    caracteristicas = caracteristicas_response.json() if caracteristicas_response.status_code == 200 else []

    return render(request, 'GestionDeProductos/index.html', {
        'productos': productos,
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas,
    })

@login_required
@permission_required('GestionDeProductos.change_producto', raise_exception=True)
def producto_edit(request, pk):
    if request.method == 'POST':
        data = {
            'codigo': request.POST['codigo'],
            'nombre': request.POST['nombre'],
            'precio': request.POST['precio'],
            'categoria': request.POST['categoria'],
            'marca': request.POST['marca'],
            'caracteristicas': []
        }
        caracteristicas = request.POST.getlist('caracteristica')
        valores = request.POST.getlist('valor')
        for caracteristica, valor in zip(caracteristicas, valores):
            if caracteristica:  # Ensure caracteristica is not empty
                data['caracteristicas'].append({'caracteristica_id': caracteristica, 'valor': valor})

        headers = {'Authorization': f'Bearer {request.session.get("jwt_token")}'}
        logger.info(f"Editing product with ID: {pk} with data: {data}")
        logger.info(f"Using JWT Token: {request.session.get('jwt_token')}")
        response = requests.put(f'{API_BASE_URL}/producto/{pk}/', json=data, headers=headers)
        if response.status_code == 200:
            producto = response.json()
            logger.info(f"Product updated successfully: {producto}")
            return redirect(f'/productos/resultado/{pk}/')
        else:
            logger.error(f"Failed to update product: {response.status_code} {response.text}")
            producto = {}
    else:
        headers = {'Authorization': f'Bearer {request.session.get("jwt_token")}'}
        logger.info(f"Fetching product with ID: {pk}")
        producto_response = requests.get(f'{API_BASE_URL}/producto/{pk}/', headers=headers)
        if producto_response.status_code == 200:
            producto = producto_response.json()
            logger.info(f"Product fetched successfully: {producto}")
            caracteristicas_response = requests.get(f'{API_BASE_URL}/caracteristicas/', headers=headers)
            categorias_response = requests.get(f'{API_BASE_URL}/categorias/', headers=headers)
            marcas_response = requests.get(f'{API_BASE_URL}/marcas/', headers=headers)
            if caracteristicas_response.status_code == 200:
                caracteristicas = caracteristicas_response.json()
            else:
                caracteristicas = []
            if categorias_response.status_code == 200:
                categorias = categorias_response.json()
            else:
                categorias = []
            if marcas_response.status_code == 200:
                marcas = marcas_response.json()
            else:
                marcas = []
            producto_caracteristicas = producto['caracteristicas']
            # Ensure the correct IDs are set for the selected category and brand
            producto['categoria_id'] = next((cat['id'] for cat in categorias if cat['name'] == producto['categoria']), None)
            producto['marca_id'] = next((mar['id'] for mar in marcas if mar['name'] == producto['marca']), None)
        else:
            logger.error(f"Failed to fetch product: {response.status_code} {response.text}")
            producto = {}
            caracteristicas = []
            categorias = []
            marcas = []
            producto_caracteristicas = []
    return render(request, 'GestionDeProductos/registro.html', {
        'producto': producto,
        'caracteristicas': caracteristicas,
        'categorias': categorias,
        'marcas': marcas,
        'producto_caracteristicas': producto_caracteristicas
    })

@login_required
@permission_required('GestionDeProductos.delete_producto', raise_exception=True)
def producto_delete(request, pk):
    headers = {'Authorization': f'Bearer {request.session.get("jwt_token")}'}
    logger.info(f"Deleting product with ID: {pk}")
    logger.info(f"Using JWT Token: {request.session.get('jwt_token')}")
    response = requests.delete(f'{API_BASE_URL}/producto/{pk}/', headers=headers)
    if response.status_code == 204:
        logger.info(f"Product deleted successfully")
    else:
        logger.error(f"Failed to delete product: {response.status_code} {response.text}")
    return redirect('index')

@login_required
@permission_required('GestionDeProductos.view_producto', raise_exception=True)
def result(request, pk):
    headers = {'Authorization': f'Bearer {request.session.get("jwt_token")}'}
    logger.info(f"Fetching product result with ID: {pk}")
    logger.info(f"Using JWT Token: {request.session.get('jwt_token')}")
    producto_response = requests.get(f'{API_BASE_URL}/producto/{pk}/', headers=headers)
    if producto_response.status_code == 200:
        producto = producto_response.json()
        logger.info(f"Product result fetched successfully: {producto}")
    else:
        producto = None
        logger.error(f"Failed to fetch product result: {producto_response.status_code} {producto_response.text}")
    return render(request, 'GestionDeProductos/result.html', {'producto': producto})

@login_required
def view_session_data(request):
    session_data = request.session.items()
    logger.info(f"Session Data: {session_data}")
    return HttpResponse(f"Session Data: {session_data}")