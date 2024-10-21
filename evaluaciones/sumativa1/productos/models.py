from django.db import models
    
class Categoria (models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Marca (models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Caracteristica (models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Producto (models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    caracteristicas = models.ManyToManyField(Caracteristica, through='ProductoCaracteristica')
    
    def __str__(self):
        return self.nombre
    
class ProductoCaracteristica (models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    caracteristica = models.ForeignKey(Caracteristica, on_delete=models.CASCADE)
    valor = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.producto.nombre} - {self.caracteristica.nombre}: {self.valor}"
    