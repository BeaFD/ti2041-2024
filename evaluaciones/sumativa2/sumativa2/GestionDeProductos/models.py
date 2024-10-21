from django.db import models

class Categoria(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Marca(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Caracteristica(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Producto(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    caracteristica = models.ManyToManyField(Caracteristica)

    def __str__(self):
        return self.name
    
class ProductoCaracteristica(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    caracteristica = models.ForeignKey(Caracteristica, on_delete=models.CASCADE)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.producto.nombre} - {self.caracteristica.name} - {self.valor}"