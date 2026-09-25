from django.urls import path
from . import views

app_name = 'gestion_inventario'

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('producto/<int:id>/', views.producto_detalle, name='producto_detalle'),
    path('agregar/', views.formulario_producto, name='formulario_producto'),
    path('guardar/', views.guardar_producto, name='guardar_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('actualizar/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('agregar-categoria/', views.formulario_categoria, name='formulario_categoria'),
    path('guardar-categoria/', views.guardar_categoria, name='guardar_categoria'),
    path('editar-categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('actualizar-categoria/<int:id>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('eliminar-categoria/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('bodegas/', views.lista_bodegas, name='lista_bodegas'),
    path('agregar-bodega/', views.formulario_bodega, name='formulario_bodega'),
    path('guardar-bodega/', views.guardar_bodega, name='guardar_bodega'),
    path('editar-bodega/<int:id>/', views.editar_bodega, name='editar_bodega'),
    path('actualizar-bodega/<int:id>/', views.actualizar_bodega, name='actualizar_bodega'),
    path('eliminar-bodega/<int:id>/', views.eliminar_bodega, name='eliminar_bodega'),
]
