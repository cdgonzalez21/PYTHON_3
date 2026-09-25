from django.shortcuts import render, redirect, get_object_or_404
from .models import Venta, DetalleVenta
from .forms import FormularioVenta
from gestion_inventario.models import Producto
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False


def lista_ventas(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    ventas = Venta.objects.all().order_by('-fecha_creacion')

    buscar = request.GET.get('buscar', '')
    if buscar:
        ventas = ventas.filter(cliente_nombre__icontains=buscar)

    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        ventas = ventas.filter(estado=estado_filtro)

    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    if fecha_desde:
        ventas = ventas.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        ventas = ventas.filter(fecha__lte=fecha_hasta)

    total_vendido = Venta.objects.aggregate(total=Sum('total'))['total'] or 0
    total_ventas = Venta.objects.count()
    ventas_pagadas = Venta.objects.filter(estado='pagada').count()
    ventas_pendientes = Venta.objects.filter(estado='pendiente').count()
    ventas_canceladas = Venta.objects.filter(estado='cancelada').count()

    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)

    ventas_hoy = Venta.objects.filter(fecha=hoy).aggregate(total=Sum('total'))['total'] or 0
    ventas_mes = Venta.objects.filter(fecha__gte=inicio_mes).aggregate(total=Sum('total'))['total'] or 0

    total_clientes = Venta.objects.values('cliente_nombre').distinct().count()

    hay_ventas = ventas.count() > 0

    data = {
        "ventas": ventas,
        "hay_ventas": hay_ventas,
        "titulo": "Modulo de Gestion de Ventas",
        "buscar": buscar,
        "estado_filtro": estado_filtro,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "total_vendido": total_vendido,
        "total_ventas": total_ventas,
        "ventas_pagadas": ventas_pagadas,
        "ventas_pendientes": ventas_pendientes,
        "ventas_canceladas": ventas_canceladas,
        "ventas_hoy": ventas_hoy,
        "ventas_mes": ventas_mes,
        "total_clientes": total_clientes,
    }
    return render(request, "list_ventas.html", data)


def formulario_venta(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    formulario = FormularioVenta()
    data = {
        "formulario": formulario,
        "titulo": "Registrar Nueva Venta",
    }
    return render(request, "formulario_venta.html", data)


def guardar_venta(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    if request.method == "POST":
        cliente_nombre = request.POST["cliente_nombre"]
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        estado = request.POST["estado"]
        producto_id = request.POST["producto"]
        cantidad = int(request.POST["cantidad"])

        producto = Producto.objects.get(id=producto_id)
        precio_unitario = producto.precio
        total = precio_unitario * cantidad

        venta = Venta.objects.create(
            cliente_nombre=cliente_nombre,
            fecha=fecha,
            hora=hora,
            estado=estado,
            total=total,
        )

        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
        )

        producto.stock -= cantidad
        producto.save()

    return redirect('gestion_ventas:lista_ventas')


def detalle_venta(request, venta_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    data = {
        "venta": venta,
        "detalles": detalles,
        "titulo": f"Detalle de Venta #{venta.id}",
    }
    return render(request, "detalle_venta.html", data)


def cancelar_venta(request, venta_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    venta = get_object_or_404(Venta, id=venta_id)
    if venta.estado != 'cancelada':
        for detalle in venta.detalles.all():
            detalle.producto.stock += detalle.cantidad
            detalle.producto.save()
        venta.estado = 'cancelada'
        venta.save()
    return redirect('gestion_ventas:lista_ventas')


def eliminar_venta(request, venta_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    venta = get_object_or_404(Venta, id=venta_id)
    if venta.estado != 'cancelada':
        for detalle in venta.detalles.all():
            detalle.producto.stock += detalle.cantidad
            detalle.producto.save()
    venta.delete()
    return redirect('gestion_ventas:lista_ventas')


def editar_venta(request, venta_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == "POST":
        venta.cliente_nombre = request.POST["cliente_nombre"]
        venta.fecha = request.POST["fecha"]
        venta.hora = request.POST["hora"]
        venta.estado = request.POST["estado"]
        venta.save()
        return redirect('gestion_ventas:lista_ventas')

    data = {
        "venta": venta,
        "titulo": f"Editar Venta #{venta.id}",
        "estados": Venta.ESTADO_CHOICES,
    }
    return render(request, "editar_venta.html", data)


def cambiar_estado(request, venta_id):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == "POST":
        nuevo_estado = request.POST["estado"]
        if nuevo_estado == 'cancelada' and venta.estado != 'cancelada':
            for detalle in venta.detalles.all():
                detalle.producto.stock += detalle.cantidad
                detalle.producto.save()
        venta.estado = nuevo_estado
        venta.save()
    return redirect('gestion_ventas:lista_ventas')


def exportar_pdf(request):
    if not request.session.get('usuario_id'):
        return redirect('gestion_usuarios:login')

    if not REPORTLAB_OK:
        return HttpResponse(
            "ReportLab no está instalado. Ejecuta: pip install reportlab",
            status=500
        )

    ventas = Venta.objects.all().order_by('-fecha_creacion')

    buscar = request.GET.get('buscar', '')
    if buscar:
        ventas = ventas.filter(cliente_nombre__icontains=buscar)
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        ventas = ventas.filter(estado=estado_filtro)
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    if fecha_desde:
        ventas = ventas.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        ventas = ventas.filter(fecha__lte=fecha_hasta)

    total_vendido = ventas.aggregate(total=Sum('total'))['total'] or 0
    total_ventas_count = ventas.count()
    pagadas = ventas.filter(estado='pagada').count()
    pendientes = ventas.filter(estado='pendiente').count()
    canceladas = ventas.filter(estado='cancelada').count()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    titulo_style = ParagraphStyle(
        'Titulo',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=6,
    )
    elements.append(Paragraph("Reporte de Ventas", titulo_style))
    elements.append(Paragraph(
        f"Generado el {timezone.now().strftime('%d/%m/%Y %H:%M')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 14))

    resumen_data = [
        ['Total Vendido', 'Total Ventas', 'Pagadas', 'Pendientes', 'Canceladas'],
        [f'${total_vendido}', str(total_ventas_count), str(pagadas), str(pendientes), str(canceladas)],
    ]
    resumen_table = Table(resumen_data, colWidths=[1.3*inch]*5)
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ede9fe')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ede9fe')]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [6]),
    ]))
    elements.append(resumen_table)
    elements.append(Spacer(1, 18))

    elements.append(Paragraph("Detalle de ventas", styles['Heading2']))
    elements.append(Spacer(1, 8))

    header = ['#', 'Cliente', 'Fecha', 'Hora', 'Total', 'Estado', 'Registrada']
    tabla_data = [header]

    estado_map = {'pagada': 'Pagada', 'pendiente': 'Pendiente', 'cancelada': 'Cancelada'}
    for v in ventas:
        tabla_data.append([
            str(v.id),
            v.cliente_nombre,
            str(v.fecha),
            str(v.hora),
            f'${v.total}',
            estado_map.get(v.estado, v.estado),
            v.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
        ])

    col_widths = [0.4*inch, 1.5*inch, 0.8*inch, 0.7*inch, 0.9*inch, 0.8*inch, 1.3*inch]
    tabla = Table(tabla_data, colWidths=col_widths, repeatRows=1)

    row_colors = []
    for i in range(1, len(tabla_data)):
        estado = ventas[i - 1].estado if i - 1 < ventas.count() else ''
        if estado == 'pagada':
            row_colors.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#dcfce7')))
        elif estado == 'cancelada':
            row_colors.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fee2e2')))
        elif estado == 'pendiente':
            row_colors.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fef9c3')))

    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        *row_colors,
    ]))
    elements.append(tabla)

    if not ventas.exists():
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("No hay ventas para mostrar.", styles['Normal']))

    doc.build(elements)
    return response
