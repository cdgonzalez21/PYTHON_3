from django.db import models

class Reporte(models.Model):
    TIPO_CHOICES = [
        ('productos', 'Productos'),
        ('gastos', 'Gastos'),
        ('usuarios', 'Usuarios'),
        ('ventas', 'Ventas'),
        ('detalle_ventas', 'Detalle de Ventas'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='productos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_generacion = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)