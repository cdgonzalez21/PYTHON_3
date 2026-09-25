from django.urls import path
from . import views

app_name = 'gestion_usuarios'

urlpatterns = [
    path('login/', views.login_usuario, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_usuario, name='logout'),
    path('index/', views.index, name='index'),
    path('empleados/', views.listar_empleados, name='listar_empleados'),
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/editar/<uuid:uuid_public>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<uuid:uuid_public>/', views.eliminar_empleado, name='eliminar_empleado'),
]
