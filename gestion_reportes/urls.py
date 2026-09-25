from django.urls import path
from . import views

app_name = 'gestion_reportes'

urlpatterns = [
    path('', views.home, name='home'),
    path('detalle_reporte/<int:reporte_id>/', views.detalle_reporte, name='detalle_reporte'),
    path('lista_reporte/', views.lista_reporte, name='lista_reporte'),
    path('formulario_reporte/', views.formulario_reporte, name='formulario_reporte'),
    path('generar_csv/', views.generar_csv, name='generar_csv'),
    path('reporte/<int:reporte_id>/eliminar/', views.eliminar_reporte, name='eliminar_reporte'),

    # Reportes CSV
    path('reporte_productos/', views.reporte_productos_csv, name='reporte_productos'),
    path('reporte_gastos/', views.reporte_gastos_csv, name='reporte_gastos'),
    path('reporte_usuarios/', views.reporte_usuarios_csv, name='reporte_usuarios'),
    path('reporte_ventas/', views.reporte_ventas_csv, name='reporte_ventas'),
    path('reporte_detalle_ventas/', views.reporte_detalle_ventas_csv, name='reporte_detalle_ventas'),

    # Acciones
    path('toggle_activo/<int:reporte_id>/', views.toggle_activo, name='toggle_activo'),
    path('descargar_csv/<int:reporte_id>/', views.descargar_csv, name='descargar_csv'),
]