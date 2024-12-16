from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from .models import Categoria, Marca, Producto, Caracteristica, ProductoCaracteristica
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta
from django.conf import settings

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return None

api = NinjaAPI(title="API de Gestión de Productos", version="1.0.0", description="API para gestionar productos, categorías, marcas y características.")

class TokenSchema(Schema):
    username: str
    password: str

class CaracteristicaSchema(Schema):
    caracteristica_id: int
    valor: str

class ProductSchema(Schema):
    codigo: str
    marca: int
    nombre: str
    precio: float
    categoria: int
    caracteristicas: list[CaracteristicaSchema]

@api.post("/token/", response=dict, tags=["Autenticación"])
def get_token(request, data: TokenSchema):
    """
    Obtener Token JWT
    - **username**: Nombre de usuario
    - **password**: Contraseña del usuario
    """
    user = authenticate(username=data.username, password=data.password)
    if user:
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return {"token": token}
    return api.create_response(request, {"detail": "Credenciales inválidas"}, status=401)

@api.get("/categorias/", response=list, tags=["Categorías"])
def get_categorias(request):
    """
    Obtener todas las categorías
    - **response**: Lista de categorías
    """
    return list(Categoria.objects.values())

@api.get("/marcas/", response=list, tags=["Marcas"])
def get_marcas(request):
    """
    Obtener todas las marcas
    - **response**: Lista de marcas
    """
    return list(Marca.objects.values())

@api.get("/productos/", response=list, tags=["Productos"])
def get_productos(request, marca: str = None, categoria: str = None):
    """
    Obtener todos los productos
    - **marca**: Filtrar productos por nombre de marca (opcional)
    - **categoria**: Filtrar productos por nombre de categoría (opcional)
    - **response**: Lista de productos con sus detalles
    """
    productos = Producto.objects.all()
    if marca:
        productos = productos.filter(marca__name__icontains=marca)
    if categoria:
        productos = productos.filter(categoria__name__icontains=categoria)
    return [
        {
            "codigo": producto.codigo,
            "marca": producto.marca.name,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "categoria": producto.categoria.name,
            "caracteristicas": [
                {
                    "name": pc.caracteristica.name,
                    "valor": pc.valor
                }
                for pc in ProductoCaracteristica.objects.filter(producto=producto)
            ]
        }
        for producto in productos
    ]

@api.get("/producto/{codigo}/", response=dict, tags=["Productos"])
def get_producto(request, codigo: str):
    """
    Obtener detalles del producto por código
    - **codigo**: Código del producto
    - **response**: Detalles del producto incluyendo características
    """
    producto = get_object_or_404(Producto, codigo=codigo)
    return {
        "codigo": producto.codigo,
        "marca": producto.marca.name,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "categoria": producto.categoria.name,
        "caracteristicas": [
            {
                "name": pc.caracteristica.name,
                "valor": pc.valor
            }
            for pc in ProductoCaracteristica.objects.filter(producto=producto)
        ]
    }

@api.post("/productos/", auth=AuthBearer(), response=dict, tags=["Productos"])
def create_producto(request, payload: ProductSchema):
    """
    Crear un nuevo producto
    - **codigo**: Código del producto
    - **marca**: ID de la marca
    - **nombre**: Nombre del producto
    - **precio**: Precio del producto
    - **categoria**: ID de la categoría
    - **caracteristicas**: Lista de características (ID y valor)
    - **response**: Mensaje de éxito y código del producto
    """
    producto = Producto.objects.create(
        codigo=payload.codigo,
        marca=Marca.objects.get(id=payload.marca),
        nombre=payload.nombre,
        precio=payload.precio,
        categoria=Categoria.objects.get(id=payload.categoria)
    )

    for caracteristica in payload.caracteristicas:
        caracteristica_obj = get_object_or_404(Caracteristica, id=caracteristica.caracteristica_id)
        ProductoCaracteristica.objects.create(
            producto=producto,
            caracteristica=caracteristica_obj,
            valor=caracteristica.valor
        )

    return {"success": True, "codigo": producto.codigo}

@api.put("/producto/{codigo}/", auth=AuthBearer(), response=dict, tags=["Productos"])
def update_producto(request, codigo: str, payload: ProductSchema):
    """
    Actualizar un producto existente
    - **codigo**: Código del producto
    - **marca**: ID de la marca
    - **nombre**: Nombre del producto
    - **precio**: Precio del producto
    - **categoria**: ID de la categoría
    - **caracteristicas**: Lista de características (ID y valor)
    - **response**: Mensaje de éxito y código del producto
    """
    producto = get_object_or_404(Producto, codigo=codigo)
    producto.marca = Marca.objects.get(id=payload.marca)
    producto.categoria = Categoria.objects.get(id=payload.categoria)
    producto.nombre = payload.nombre
    producto.precio = payload.precio
    producto.save()

    # Actualizar características
    existing_caracteristicas = {pc.caracteristica.id: pc for pc in ProductoCaracteristica.objects.filter(producto=producto)}
    for caracteristica in payload.caracteristicas:
        if caracteristica.caracteristica_id in existing_caracteristicas:
            pc = existing_caracteristicas[caracteristica.caracteristica_id]
            pc.valor = caracteristica.valor
            pc.save()
        else:
            caracteristica_obj = get_object_or_404(Caracteristica, id=caracteristica.caracteristica_id)
            ProductoCaracteristica.objects.create(
                producto=producto,
                caracteristica=caracteristica_obj,
                valor=caracteristica.valor
            )

    # Eliminar características removidas
    for caracteristica_id in existing_caracteristicas:
        if caracteristica_id not in [c.caracteristica_id for c in payload.caracteristicas]:
            existing_caracteristicas[caracteristica_id].delete()

    return {"success": True, "codigo": producto.codigo}

@api.patch("/producto/{codigo}/", auth=AuthBearer(), response=dict, tags=["Productos"])
def partial_update_producto(request, codigo: str, payload: ProductSchema):
    """
    Actualizar parcialmente un producto existente
    - **codigo**: Código del producto
    - **marca**: ID de la marca (opcional)
    - **nombre**: Nombre del producto (opcional)
    - **precio**: Precio del producto (opcional)
    - **categoria**: ID de la categoría (opcional)
    - **caracteristicas**: Lista de características (ID y valor) (opcional)
    - **response**: Mensaje de éxito y código del producto
    """
    producto = get_object_or_404(Producto, codigo=codigo)
    if 'marca' in payload.dict():
        producto.marca = Marca.objects.get(id=payload.marca)
    if 'categoria' in payload.dict():
        producto.categoria = Categoria.objects.get(id=payload.categoria)
    for key, value in payload.dict().items():
        if key in ['marca', 'categoria', 'caracteristicas']:
            continue
        setattr(producto, key, value)
    producto.save()

    # Actualizar características
    if "caracteristicas" in payload.dict():
        existing_caracteristicas = {pc.caracteristica.id: pc for pc in ProductoCaracteristica.objects.filter(producto=producto)}
        for caracteristica in payload.caracteristicas:
            if caracteristica.caracteristica_id in existing_caracteristicas:
                pc = existing_caracteristicas[caracteristica.caracteristica_id]
                pc.valor = caracteristica.valor
                pc.save()
            else:
                caracteristica_obj = get_object_or_404(Caracteristica, id=caracteristica.caracteristica_id)
                ProductoCaracteristica.objects.create(
                    producto=producto,
                    caracteristica=caracteristica_obj,
                    valor=caracteristica.valor
                )

        # Eliminar características removidas
        for caracteristica_id in existing_caracteristicas:
            if caracteristica_id not in [c.caracteristica_id for c in payload.caracteristicas]:
                existing_caracteristicas[caracteristica_id].delete()

    return {"success": True, "codigo": producto.codigo}

@api.delete("/producto/{codigo}/", auth=AuthBearer(), response=dict, tags=["Productos"])
def delete_producto(request, codigo: str):
    """
    Eliminar un producto por código
    - **codigo**: Código del producto
    - **response**: Mensaje de éxito
    """
    producto = get_object_or_404(Producto, codigo=codigo)
    producto.delete()
    return {"success": True}