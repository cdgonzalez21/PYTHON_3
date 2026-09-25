import uuid
from django.db import models


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Modulo(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    nombre = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    fecha_nacimiento = models.DateField()
    hora_creacion = models.TimeField(auto_now_add=True)
    fecha_creacion =  models.DateField(auto_now_add=True, null=True)
    activo = models.BooleanField(default=True)
    confirmado = models.BooleanField(null=True, blank=True)
    rol = models.ForeignKey(Rol,on_delete=models.PROTECT,related_name="usuarios")
    modulos = models.ManyToManyField(Modulo,blank=True)
    uuid_public = models.UUIDField(default=uuid.uuid4,editable=False,unique=True,primary_key=True)

    def __str__(self):
        return f"Usuario: {self.nombre}"

