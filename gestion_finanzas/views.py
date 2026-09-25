from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.http import HttpResponse
from . import models
from .forms import crear_gastos
from  gestion_ventas.models import Venta
from gestion_inventario.models import Producto
from django.db.models import Sum,F
from django.db.models.functions import TruncMonth


# Create your views here.

def inicio (request):
    return render(request,'inicio.html')

def gastos (request):

    data = models.Gasto.objects.all()
    return render(request, 'gastos_finanzas.html', {'data': data})

def crear_gasto(request):
    if request.method == 'POST':
        form = crear_gastos(request.POST)
        if form.is_valid():
            models.Gasto.objects.create(
                descripcion=form.cleaned_data['descripcion'],
                monto=form.cleaned_data['monto'],
                fecha=form.cleaned_data['fecha'],
                tipo=form.cleaned_data['tipo'] 
            )
            return redirect('gestion_finanzas:gasto')
    else:
        form = crear_gastos()

    return render(request, 'crear.html', {'form': form})

def eliminar_gasto(request, id):

    gasto = get_object_or_404(models.Gasto, id=id)

    gasto.delete()

    return redirect('gestion_finanzas:gasto')

# views.py

from django.shortcuts import render

from django.db.models import Sum
from django.utils.timezone import now

from gestion_ventas.models import Venta, DetalleVenta
from .models import Gasto


def dashboard_finanzas(request):

    fecha_actual = now()

    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year


    ventas_mes = (
        Venta.objects
        .filter(
            fecha__month=mes_actual,
            fecha__year=anio_actual,
            estado='pagada'
        )
        .aggregate(total=Sum('total'))
    )

    total_mes = ventas_mes['total'] or 0


    productos_mas_vendidos = (
        DetalleVenta.objects
        .filter(
            venta__fecha__month=mes_actual,
            venta__fecha__year=anio_actual,
            venta__estado='pagada'
        )
        .values('producto__nombre')
        .annotate(
            total_vendidos=Sum('cantidad')
        )
        .order_by('-total_vendidos')[:10]
    )


    gastos_mayores = (
        Gasto.objects
        .filter(
            fecha__month=mes_actual,
            fecha__year=anio_actual
        )
        .order_by('-monto')[:10]
    )


    gastos_mes = (
        Gasto.objects
        .filter(
            fecha__month=mes_actual,
            fecha__year=anio_actual
        )
        .aggregate(total=Sum('monto'))
    )

    total_gastos = gastos_mes['total'] or 0


    balance = total_mes - total_gastos


    return render(request, 'dashboard_finanzas.html', {

        'total_mes': total_mes,

        'productos_mas_vendidos': productos_mas_vendidos,

        'gastos_mayores': gastos_mayores,

        'total_gastos': total_gastos,

        'balance': balance,

    })

def ingresos(request):

    fecha_actual = now()

    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year


    ventas = (
        Venta.objects
        .all()
        .order_by('-fecha', '-hora')
    )


    ingresos_mes = (
        Venta.objects
        .filter(
            fecha__month=mes_actual,
            fecha__year=anio_actual,
            estado='pagada'
        )
        .aggregate(total=Sum('total'))
    )

    total_mes = ingresos_mes['total'] or 0


    ingresos_anio = (
        Venta.objects
        .filter(
            fecha__year=anio_actual,
            estado='pagada'
        )
        .aggregate(total=Sum('total'))
    )

    total_anio = ingresos_anio['total'] or 0


    ventas_pagadas = (
        Venta.objects
        .filter(estado='pagada')
        .count()
    )


    ventas_pendientes = (
        Venta.objects
        .filter(estado='pendiente')
        .count()
    )


    return render(request, 'ingresos.html', {

        'ventas': ventas,

        'total_mes': total_mes,

        'total_anio': total_anio,

        'ventas_pagadas': ventas_pagadas,

        'ventas_pendientes': ventas_pendientes,

    })


def inventario_financiero(request):

    productos = (
        Producto.objects
        .annotate(
            valor_total=F('stock') * F('precio')
        )
        .order_by('-valor_total')
    )


    valor_inventario = (
        Producto.objects
        .annotate(
            valor_total=F('stock') * F('precio')
        )
        .aggregate(
            total=Sum('valor_total')
        )
    )

    total_inventario = valor_inventario['total'] or 0


    agotados = (
        Producto.objects
        .filter(stock=0)
        .count()
    )


    stock_bajo = (
        Producto.objects
        .filter(stock__lte=5)
        .count()
    )



    producto_costoso = (
        Producto.objects
        .order_by('-precio')
        .first()
    )


    return render(request, 'inventario_financiero.html', {

        'productos': productos,

        'total_inventario': total_inventario,

        'agotados': agotados,

        'stock_bajo': stock_bajo,

        'producto_costoso': producto_costoso,

    })


def reportes_financieros(request):

    fecha_inicio = request.GET.get('inicio')
    fecha_fin = request.GET.get('fin')


    ventas = Venta.objects.filter(estado='pagada')
    gastos = Gasto.objects.all()



    if fecha_inicio and fecha_fin:

        ventas = ventas.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        )

        gastos = gastos.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        )


    total_ventas = (
        ventas.aggregate(
            total=Sum('total')
        )['total'] or 0
    )


    total_gastos = (
        gastos.aggregate(
            total=Sum('monto')
        )['total'] or 0
    )


    balance = total_ventas - total_gastos


    return render(request, 'reportes_financieros.html', {

        'ventas': ventas,

        'gastos': gastos,

        'total_ventas': total_ventas,

        'total_gastos': total_gastos,

        'balance': balance,

    })

def alertas_financieras(request):

  
    agotados = (
        Producto.objects
        .filter(stock=0)
    )




    stock_bajo = (
        Producto.objects
        .filter(stock__lte=5, stock__gt=0)
    )


    
    ventas_pendientes = (
        Venta.objects
        .filter(estado='pendiente')
        .order_by('-fecha')
    )


    

    gastos_altos = (
        Gasto.objects
        .filter(monto__gte=1000000)
        .order_by('-monto')
    )


    return render(request, 'alertas_financieras.html', {

        'agotados': agotados,

        'stock_bajo': stock_bajo,

        'ventas_pendientes': ventas_pendientes,

        'gastos_altos': gastos_altos,

    })