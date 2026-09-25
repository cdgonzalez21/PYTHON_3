from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reporte
from datetime import datetime, timedelta
import csv
from . import models
from gestion_inventario.models import Producto
from gestion_usuarios.models import Usuario
from gestion_ventas.models import Venta, DetalleVenta

try:
    from gestion_finanzas.models import Gasto
    GASTO_OK = True
except ImportError:
    GASTO_OK = False


def home(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')
    return render(request, 'home_reportes.html')


def lista_reporte(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    reporte_id = request.GET.get('id')
    if reporte_id:
        return redirect('gestion_reportes:detalle_reporte', reporte_id=reporte_id)

    nombre = request.GET.get('nombre')
    if nombre:
        reporte = models.Reporte.objects.filter(nombre__icontains=nombre).first()
        if reporte:
            return redirect('gestion_reportes:detalle_reporte', reporte_id=reporte.id)

    data = models.Reporte.objects.all()
    data_envio = {
        'reportes': data
    }
    return render(request, 'lista_reporte.html', data_envio)


def detalle_reporte(request, reporte_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    data = models.Reporte.objects.get(id=reporte_id)
    data_envio = {
        'reporte': data,
        'existe': True
    }
    return render(request, 'detalle_reporte.html', data_envio)


def formulario_reporte(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    if request.method == "POST":
        nombre = request.POST["nombre"]
        tipo = request.POST["tipo"]
        fecha_inicio = request.POST["fecha_inicio"]
        fecha_fin = request.POST["fecha_fin"]
        descripcion = request.POST["descripcion"]
        activo = request.POST.get("activo") == "on"

        Reporte.objects.create(
            nombre=nombre,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            descripcion=descripcion,
            activo=activo,
        )
        return redirect('gestion_reportes:lista_reporte')
    return render(request, "formulario_reporte.html")


def generar_csv(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    reportes_activos = models.Reporte.objects.filter(activo=True)
    data_envio = {
        'reportes': reportes_activos
    }
    return render(request, 'generar_csv.html', data_envio)


def toggle_activo(request, reporte_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    reporte = get_object_or_404(models.Reporte, id=reporte_id)
    reporte.activo = not reporte.activo
    reporte.save()
    return redirect('gestion_reportes:lista_reporte')


#reportes rapidos 

def reporte_productos_csv(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=productos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nombre', 'Stock', 'Precio', 'Garantía (meses)', 'Peso (kg)', 'Categoría', 'Bodega','Fecha creación'])
    for producto in Producto.objects.select_related('categoria', 'bodega').all():
        writer.writerow([
            producto.id,
            producto.nombre,
            producto.stock,
            producto.precio,
            producto.garantia_meses,
            producto.peso_kg,
            producto.categoria.nombre if producto.categoria else '',
            producto.bodega.nombre if producto.bodega else 'Sin bodega',
            producto.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        ])
    return response


def reporte_gastos_csv(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    if not GASTO_OK:
        return HttpResponse('App de finanzas no disponible')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=gastos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Descripción', 'Monto', 'Fecha', 'Tipo de Gasto'])
    for gasto in Gasto.objects.all():
        writer.writerow([
            gasto.id,
            gasto.descripcion,
            gasto.monto,
            gasto.fecha.strftime("%Y-%m-%d"),
            gasto.tipo.nombre
        ])
    return response


def reporte_usuarios_csv(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=usuarios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['UUID', 'Nombre', 'Email', 'Fecha Nacimiento', 'Activo', 'Confirmado', 'Rol','Fecha creación'])
    for usuario in Usuario.objects.all():
        writer.writerow([
            str(usuario.uuid_public),
            usuario.nombre,
            usuario.email,
            usuario.fecha_nacimiento.strftime("%Y-%m-%d"),
            "Sí" if usuario.activo else "No",
            "Sí" if usuario.confirmado else "No",
            usuario.rol.nombre,
            usuario.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        ])
    return response


def reporte_ventas_csv(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=ventas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID Venta', 'Fecha', 'Hora', 'Cliente', 'Total'])
    for venta in Venta.objects.all():
        writer.writerow([
            venta.id,
            venta.fecha.strftime("%Y-%m-%d"),
            venta.hora.strftime("%H:%M:%S"),
            venta.cliente_nombre,
            venta.total
        ])
    return response


def reporte_detalle_ventas_csv(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=detalle_ventas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID Detalle', 'ID Venta', 'Producto', 'Cantidad', 'Precio Unitario', 'Subtotal','Fecha creación'])
    for detalle in DetalleVenta.objects.all():
        writer.writerow([
            detalle.id,
            detalle.venta.id,
            detalle.producto.nombre,
            detalle.cantidad,
            detalle.precio_unitario,
            detalle.cantidad * detalle.precio_unitario,
            detalle.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        ])
    return response


#funcion de descarga 

def descargar_csv(request, reporte_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    reporte = get_object_or_404(models.Reporte, id=reporte_id)

    # Si el reporte fue creado por el usuario (personalizado)
    if reporte.fecha_inicio and reporte.fecha_fin:
        if reporte.tipo == 'ventas':
            return reporte_ventas_personalizado_csv(request, reporte)
        elif reporte.tipo == 'detalle_ventas':
            return reporte_detalle_ventas_personalizado_csv(request, reporte)
        elif reporte.tipo == 'gastos':
            return reporte_gastos_personalizado_csv(request, reporte)
        elif reporte.tipo == 'usuarios':
            return reporte_usuarios_personalizado_csv(request, reporte)
        elif reporte.tipo == 'productos':
            return reporte_productos_personalizado_csv(request, reporte)

    # Si no tiene fechas → es un reporte rápido
    if reporte.tipo == 'productos':
        return reporte_productos_csv(request)
    elif reporte.tipo == 'gastos':
        return reporte_gastos_csv(request)
    elif reporte.tipo == 'usuarios':
        return reporte_usuarios_csv(request)
    elif reporte.tipo == 'ventas':
        return reporte_ventas_csv(request)
    elif reporte.tipo == 'detalle_ventas':
        return reporte_detalle_ventas_csv(request)

    return redirect('gestion_reportes:generar_csv')


def eliminar_reporte(request, reporte_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    reporte = get_object_or_404(Reporte, id=reporte_id)
    reporte.delete()
    return redirect('gestion_reportes:lista_reporte')


#reportes personalizados 

def reporte_ventas_personalizado_csv(request, reporte):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=ventas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID Venta', 'Fecha', 'Hora', 'Cliente', 'Total'])

    ventas = Venta.objects.all()
    if reporte.fecha_inicio and reporte.fecha_fin:
        ventas = ventas.filter(
            fecha__gte=reporte.fecha_inicio,
            fecha__lt=reporte.fecha_fin + timedelta(days=1)
        )

    for venta in ventas:
        writer.writerow([
            venta.id,
            venta.fecha.strftime("%Y-%m-%d"),
            venta.hora.strftime("%H:%M:%S"),
            venta.cliente_nombre,
            venta.total,
            
        ])
    return response


def reporte_productos_personalizado_csv(request, reporte):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=productos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nombre', 'Stock', 'Precio', 'Garantía (meses)', 'Peso (kg)', 'Categoría', 'Bodega','Fecha creación'])

    productos = Producto.objects.select_related('categoria', 'bodega').all()
    if reporte.fecha_inicio and reporte.fecha_fin:
        productos = productos.filter(
            fecha_creacion__gte=reporte.fecha_inicio,
            fecha_creacion__lt=reporte.fecha_fin + timedelta(days=1)
        )

    for producto in productos:
        writer.writerow([
            producto.id,
            producto.nombre,
            producto.stock,
            producto.precio,
            producto.garantia_meses,
            producto.peso_kg,
            producto.categoria.nombre if producto.categoria else '',
            producto.bodega.nombre if producto.bodega else 'Sin bodega',
            producto.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        ])
    return response


def reporte_usuarios_personalizado_csv(request, reporte):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=usuarios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['UUID', 'Nombre', 'Email', 'Fecha Nacimiento', 'Activo', 'Confirmado', 'Rol','Fecha creación'])

    usuarios = Usuario.objects.all()
    if reporte.fecha_inicio and reporte.fecha_fin:
        usuarios = usuarios.filter(
            fecha_creacion__gte=reporte.fecha_inicio,
            fecha_creacion__lt=reporte.fecha_fin + timedelta(days=1)
        )

    for usuario in usuarios:
        writer.writerow([
            str(usuario.uuid_public),
            usuario.nombre,
            usuario.email,
            usuario.fecha_nacimiento.strftime("%Y-%m-%d"),
            "Sí" if usuario.activo else "No",
            "Sí" if usuario.confirmado else "No",
            usuario.rol.nombre,
             usuario.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        ])
    return response


def reporte_gastos_personalizado_csv(request, reporte):
    if not GASTO_OK:
        return HttpResponse('App de finanzas no disponible')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=gastos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Descripción', 'Monto', 'Fecha', 'Tipo de Gasto'])

    gastos = Gasto.objects.all()
    if reporte.fecha_inicio and reporte.fecha_fin:
        gastos = gastos.filter(
            fecha__gte=reporte.fecha_inicio,
            fecha__lt=reporte.fecha_fin + timedelta(days=1)
        )

    for gasto in gastos:
        writer.writerow([
            gasto.id,
            gasto.descripcion,
            gasto.monto,
            gasto.fecha.strftime("%Y-%m-%d"),
            gasto.tipo.nombre
        ])
    return response


def reporte_detalle_ventas_personalizado_csv(request, reporte):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename=detalle_ventas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    response.write('﻿')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID Detalle', 'ID Venta', 'Producto', 'Cantidad', 'Precio Unitario', 'Subtotal','Fecha creación'])

    detalles = DetalleVenta.objects.select_related('venta', 'producto').all()
    if reporte.fecha_inicio and reporte.fecha_fin:
        detalles = detalles.filter(
            venta__fecha__gte=reporte.fecha_inicio,
            venta__fecha__lt=reporte.fecha_fin + timedelta(days=1)
        )

    for detalle in detalles:
        writer.writerow([
            detalle.id,
            detalle.venta.id,
            detalle.producto.nombre,
            detalle.cantidad,
            detalle.precio_unitario,
            detalle.cantidad * detalle.precio_unitario,
            detalle.venta.fecha.strftime("%Y-%m-%d %H:%M:%S")
        ])
    return response
