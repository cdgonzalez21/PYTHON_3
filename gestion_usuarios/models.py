from djongo import models


class Rol(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Usuario(models.Model):
    nombre = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    fecha_nacimiento = models.DateField(auto_now_add=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    roles = models.EmbeddedField(model_container=Rol)

    def __str__(self):
        return self.nombre


