from django import forms
from .models import TipoGasto

class crear_gastos(forms.Form):

    descripcion = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    monto = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=0
    )

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    tipo = forms.ModelChoiceField(
        queryset=TipoGasto.objects.all(),
        empty_label="Seleccione un tipo"
    )
 
 

