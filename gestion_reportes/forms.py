from django import forms

class FormularioReportes(forms.Form):
    TIPO_CHOICES = [
        ('productos', 'Productos'),
        ('gastos', 'Gastos'),
        ('usuarios', 'Usuarios'),
        ('ventas', 'Ventas'),
        ('detalle_ventas', 'Detalle de Ventas'),
    ]

    nombre = forms.CharField(max_length=100)
    tipo = forms.ChoiceField(choices=TIPO_CHOICES)
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    activo = forms.BooleanField(required=False, initial=True)