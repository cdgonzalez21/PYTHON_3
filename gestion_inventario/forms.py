# pyrefly: ignore [missing-import]
from django import forms
from gestion_inventario.models import Categoria, Bodega

class FormularioProducto(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    precio = forms.DecimalField(label="Precio")
    stock = forms.IntegerField(label="Stock")
    garantia_meses = forms.IntegerField(label="Garantia (meses)")
    categoria = forms.ModelChoiceField(
        label="Categoria",
        queryset=Categoria.objects.all()
    )
    bodega = forms.ModelChoiceField(
        label="Bodega",
        queryset=Bodega.objects.all(),
        required=False
    )

class FormularioCategoria(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=60)
    descripcion = forms.CharField(label="Descripcion", required=False)

class FormularioBodega(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    ubicacion = forms.CharField(label="Ubicacion", max_length=200)
