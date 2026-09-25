from django import forms
from .models import Rol, Modulo


class RegistroUsuarioForm(forms.Form):
    nombre = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    modulos = forms.ModelMultipleChoiceField(queryset=Modulo.objects.all(),
    widget=forms.CheckboxSelectMultiple,required=False)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

