from django.urls import path
from . import views

app_name = 'gestion_ventas'

urlpatterns = [
    path('', views.lista_ventas, name='lista_ventas'),
    path('nueva/', views.formulario_venta, name='formulario_venta'),
    path('guardar/', views.guardar_venta, name='guardar_venta'),
    path('detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('cancelar/<int:venta_id>/', views.cancelar_venta, name='cancelar_venta'),
    path('eliminar/<int:venta_id>/', views.eliminar_venta, name='eliminar_venta'),
    path('editar/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('estado/<int:venta_id>/', views.cambiar_estado, name='cambiar_estado'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
]
