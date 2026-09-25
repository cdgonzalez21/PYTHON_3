from . import views
from django.urls import path
app_name = 'gestion_finanzas'
urlpatterns = [
    path('', views.dashboard_finanzas, name = 'dashboard' ),
    path('gastos/',views.gastos, name = 'gasto' ),
    path('gastos/crear/',views.crear_gasto, name = 'crear' ),
    path('gastos/eliminar/<int:id>',views.eliminar_gasto, name = 'eliminar' ),
    path('ingresos/',views.ingresos,name='ingresos'),
    path('inventario/',views.inventario_financiero,name='inventario_financiero'),   
    path('reportes/',views.reportes_financieros,name='reportes'), 
    path('alertas/',views.alertas_financieras,name='alertas'), 
         
         

   
]
