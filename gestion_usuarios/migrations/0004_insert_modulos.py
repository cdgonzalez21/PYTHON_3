from django.db import migrations


def insertar_modulos(apps, schema_editor):
    Modulo = apps.get_model('gestion_usuarios', 'Modulo')
    nombres = ['Inventario', 'Ventas', 'Reportes', 'Finanzas', 'Gestión de usuarios']
    for nombre in nombres:
        Modulo.objects.get_or_create(nombre=nombre)


def eliminar_modulos(apps, schema_editor):
    Modulo = apps.get_model('gestion_usuarios', 'Modulo')
    Modulo.objects.filter(
        nombre__in=['Inventario', 'Ventas', 'Reportes', 'Finanzas', 'Gestión de usuarios']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_usuarios', '0003_usuario_fecha_creacion'),
    ]

    operations = [
        migrations.RunPython(insertar_modulos, eliminar_modulos),
    ]
