from django import forms

class RegistroUsuarioForm(forms.Form):
    nombre = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    rol_nombre = forms.CharField(max_length=80, label="Nombre del Rol")
    rol_descripcion = forms.CharField(max_length=100, label="Descripción del Rol", required=False)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
