# pyrefly: ignore [missing-import]
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    garantia_meses = models.PositiveIntegerField()
    peso_kg = models.FloatField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    bodega = models.ForeignKey(Bodega, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Producto: {self.nombre}"
