from django.shortcuts import render, redirect
from gestion_inventario.models import Producto, Categoria, Bodega
from gestion_inventario import forms

def home(request):
    data = {
        'total_productos': Producto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_bodegas': Bodega.objects.count(),
        'total_agotados': Producto.objects.filter(stock=0).count(),
    }
    return render(request, 'home_inventario.html', data)

def lista_productos(request):
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')

    if categoria_id:
        productos = Producto.objects.filter(categoria_id=categoria_id).select_related('categoria', 'bodega')
        categoria_seleccionada = int(categoria_id)
    else:
        productos = Producto.objects.all().select_related('categoria', 'bodega')
        categoria_seleccionada = None

    data = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada
    }
    return render(request, 'lista_productos.html', data)

def lista_categorias(request):
    categorias = Categoria.objects.all()
    data = {
        'categorias': categorias
    }
    return render(request, 'lista_categorias.html', data)

def producto_detalle(request, id):
    producto = Producto.objects.get(id=id)
    data = {
        'producto': producto
    }
    return render(request, 'producto_detalle.html', data)

def formulario_producto(request):
    data = {
        'formulario': forms.FormularioProducto
    }
    return render(request, 'formulario_producto.html', data)

def guardar_producto(request):
    nombre = request.POST["nombre"]
    precio = request.POST["precio"]
    stock = request.POST["stock"]
    garantia_meses = request.POST["garantia_meses"]
    categoria_id = request.POST["categoria"]
    bodega_id = request.POST.get("bodega") or None

    Producto.objects.create(
        nombre=nombre,
        precio=precio,
        stock=stock,
        garantia_meses=garantia_meses,
        categoria_id=categoria_id,
        bodega_id=bodega_id
    )

    return redirect('gestion_inventario:lista_productos')

def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    data = {
        'formulario': forms.FormularioProducto,
        'producto': producto
    }
    return render(request, 'editar_producto.html', data)

def actualizar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.nombre = request.POST["nombre"]
    producto.precio = request.POST["precio"]
    producto.stock = request.POST["stock"]
    producto.garantia_meses = request.POST["garantia_meses"]
    producto.categoria_id = request.POST["categoria"]
    producto.bodega_id = request.POST.get("bodega") or None
    producto.save()

    return redirect('gestion_inventario:lista_productos')

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('gestion_inventario:lista_productos')

def formulario_categoria(request):
    data = {
        'formulario': forms.FormularioCategoria
    }
    return render(request, 'formulario_categoria.html', data)

def guardar_categoria(request):
    nombre = request.POST["nombre"]
    descripcion = request.POST["descripcion"]

    Categoria.objects.create(
        nombre=nombre,
        descripcion=descripcion
    )

    return redirect('gestion_inventario:lista_categorias')

def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    data = {
        'formulario': forms.FormularioCategoria,
        'categoria': categoria
    }
    return render(request, 'editar_categoria.html', data)

def actualizar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.nombre = request.POST["nombre"]
    categoria.descripcion = request.POST["descripcion"]
    categoria.save()
    return redirect('gestion_inventario:lista_categorias')

def eliminar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('gestion_inventario:lista_categorias')

# --- Bodegas ---

def lista_bodegas(request):
    bodegas = Bodega.objects.all()
    data = {
        'bodegas': bodegas
    }
    return render(request, 'lista_bodegas.html', data)

def formulario_bodega(request):
    data = {
        'formulario': forms.FormularioBodega
    }
    return render(request, 'formulario_bodega.html', data)

def guardar_bodega(request):
    nombre = request.POST["nombre"]
    ubicacion = request.POST["ubicacion"]

    Bodega.objects.create(
        nombre=nombre,
        ubicacion=ubicacion
    )

    return redirect('gestion_inventario:lista_bodegas')

def editar_bodega(request, id):
    bodega = Bodega.objects.get(id=id)
    data = {
        'formulario': forms.FormularioBodega,
        'bodega': bodega
    }
    return render(request, 'editar_bodega.html', data)

def actualizar_bodega(request, id):
    bodega = Bodega.objects.get(id=id)
    bodega.nombre = request.POST["nombre"]
    bodega.ubicacion = request.POST["ubicacion"]
    bodega.save()
    return redirect('gestion_inventario:lista_bodegas')

def eliminar_bodega(request, id):
    bodega = Bodega.objects.get(id=id)
    bodega.delete()
    return redirect('gestion_inventario:lista_bodegas')
