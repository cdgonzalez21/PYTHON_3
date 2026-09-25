from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm, LoginForm
from .models import Usuario, Rol


def registro(request):

    if request.method == 'POST':

        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            if Usuario.objects.filter(email=data['email']).exists():
                messages.error(request, "El email ya está registrado")
                return render(request, 'gestion_usuarios/registro.html', {'form': form})

            rol_empleado = Rol.objects.get(nombre="Empleado")

            Usuario.objects.create(
                nombre=data['nombre'],
                email=data['email'],
                password=data['password'],
                fecha_nacimiento=data.get('fecha_nacimiento'),
                activo=data.get('activo', False),
                confirmado=data.get('confirmado', False),
                rol=rol_empleado
            )

            messages.success(request, "Usuario registrado correctamente")
            return redirect('gestion_usuarios:login')

    else:
        form = RegistroUsuarioForm()

    return render(request, 'gestion_usuarios/registro.html', {'form': form})


def login_usuario(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                usuario = Usuario.objects.get(email=email)

                if usuario.password == password:

                    request.session['usuario_id'] = str(usuario.pk)
                    request.session['usuario_nombre'] = usuario.nombre
                    request.session['usuario_rol'] = usuario.rol.nombre

                    return redirect('gestion_usuarios:index')

                messages.error(request, "Contraseña incorrecta")

            except Usuario.DoesNotExist:
                messages.error(request, "El usuario no existe")

    else:
        form = LoginForm()

    return render(request, 'gestion_usuarios/login.html', {'form': form})


def logout_usuario(request):
    request.session.flush()
    return redirect('gestion_usuarios:login')


def index(request):

    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('gestion_usuarios:login')

    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('gestion_usuarios:login')

    modulos = list(usuario.modulos.values_list('nombre', flat=True))

    if usuario.rol.nombre == "Admin":

        modulos_admin = [
            "Inventario",
            "Reportes",
            "Ventas",
            "Finanzas",
            "Gestión de usuarios",
        ]

        modulos = list(set(modulos + modulos_admin))

    return render(request, 'index.html', {'usuario': usuario,'modulos': modulos})


def listar_empleados(request):

    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('gestion_usuarios:login')

    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('gestion_usuarios:login')

    if usuario.rol.nombre != "Admin":
        return redirect('gestion_usuarios:index')

    empleados = Usuario.objects.filter(rol__nombre="Empleado")

    return render(request,
                  'gestion_usuarios/listar_empleados.html',
                  {'empleados': empleados})


def crear_empleado(request):

    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('gestion_usuarios:login')

    usuario = Usuario.objects.get(pk=usuario_id)

    if usuario.rol.nombre != "Admin":
        return redirect('gestion_usuarios:index')

    if request.method == 'POST':

        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            rol_empleado = Rol.objects.get(nombre="Empleado")

            empleado = Usuario.objects.create(
                nombre=data['nombre'],
                email=data['email'],
                password=data['password'],
                fecha_nacimiento=data['fecha_nacimiento'],
                activo=True,
                confirmado=True,
                rol=rol_empleado
            )

            empleado.modulos.set(data['modulos'])

            return redirect('gestion_usuarios:listar_empleados')

    else:
        form = RegistroUsuarioForm()

    return render(request,
                  'gestion_usuarios/registro.html',
                  {'form': form})


def editar_empleado(request, uuid_public):

    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('gestion_usuarios:login')

    usuario = Usuario.objects.get(pk=usuario_id)

    if usuario.rol.nombre != "Admin":
        return redirect('gestion_usuarios:index')

    try:
        empleado = Usuario.objects.get(pk=uuid_public)
    except Usuario.DoesNotExist:
        return redirect('gestion_usuarios:listar_empleados')

    if request.method == 'POST':

        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            empleado.nombre = data['nombre']
            empleado.email = data['email']
            empleado.password = data['password']
            empleado.fecha_nacimiento = data['fecha_nacimiento']
            empleado.save()
            empleado.modulos.set(data['modulos'])

            return redirect('gestion_usuarios:listar_empleados')

    else:

        form = RegistroUsuarioForm(initial={
            'nombre': empleado.nombre,
            'email': empleado.email,
            'password': empleado.password,
            'fecha_nacimiento': empleado.fecha_nacimiento,
            'modulos': empleado.modulos.all(),
        })

    return render(request,
                  'gestion_usuarios/registro.html',
                  {'form': form, 'editar': True})


def eliminar_empleado(request, uuid_public):

    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('gestion_usuarios:login')

    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('gestion_usuarios:login')

    if usuario.rol.nombre != "Admin":
        return redirect('gestion_usuarios:index')

    try:
        empleado = Usuario.objects.get(pk=uuid_public)
        empleado.delete()
    except Usuario.DoesNotExist:
        pass

    return redirect('gestion_usuarios:listar_empleados')
