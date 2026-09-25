from django import forms
from .models import Venta, DetalleVenta
from gestion_inventario.models import Producto

class FormularioVenta(forms.Form):
    cliente_nombre = forms.CharField(
        label='Nombre del cliente',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre completo'})
    )
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hora = forms.TimeField(
        label='Hora',
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    estado = forms.ChoiceField(
        label='Estado',
        choices=Venta.ESTADO_CHOICES
    )
    producto = forms.ModelChoiceField(
        label='Producto',
        queryset=Producto.objects.all()
    )
    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        initial=1
    )