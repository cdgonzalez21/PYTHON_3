from django.db import models

class TipoGasto(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Gasto(models.Model):
    descripcion = models.CharField(max_length=150)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateField()
    tipo = models.ForeignKey( TipoGasto, on_delete=models.PROTECT, related_name="gastos" )

    def __str__(self):
      return f"{self.descripcion} - ${self.monto} ({self.fecha})"