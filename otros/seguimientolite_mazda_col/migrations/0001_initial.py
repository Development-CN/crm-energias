# Generated by Django 3.2.7 on 2021-09-21 20:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ActividadesAdicionales',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=50, null=True)),
                ('item', models.CharField(blank=True, max_length=250, null=True)),
                ('id_item', models.CharField(blank=True, max_length=50, null=True)),
                ('estado', models.CharField(blank=True, max_length=50, null=True)),
                ('cantidad', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=50, null=True)),
                ('no_parte', models.CharField(blank=True, max_length=50, null=True)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('total_iva', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('porcentaje_descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('existencia', models.CharField(blank=True, max_length=10, null=True)),
                ('localizacion', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_hora_fin', models.DateTimeField(blank=True, null=True)),
                ('fecha_hora_actualizacion', models.DateTimeField(blank=True, null=True)),
                ('uts', models.IntegerField(blank=True, null=True)),
                ('monto_refaccion', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('monto_mo', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
            ],
            options={
                'db_table': 'actividades_adicionales',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ListaItemsAdicionales',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_item', models.BigIntegerField(blank=True, null=True)),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('familia', models.IntegerField(blank=True, null=True)),
                ('orden', models.IntegerField(blank=True, null=True)),
                ('costo_repuestos', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('costo_mo', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('activo', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lista_items_adicionales',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VInformacion',
            fields=[
                ('no_orden', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('vin', models.CharField(blank=True, max_length=100, null=True)),
                ('kilometraje', models.CharField(blank=True, max_length=100, null=True)),
                ('asesor', models.CharField(blank=True, max_length=150, null=True)),
                ('cliente', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('placas', models.CharField(blank=True, max_length=100, null=True)),
                ('vehiculo', models.CharField(blank=True, max_length=100, null=True)),
                ('modelo', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_hora_ingreso', models.DateTimeField(blank=True, null=True)),
                ('tecnico', models.CharField(blank=True, max_length=250, null=True)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'v_informacion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VInterfazDms',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('numero', models.BigIntegerField(blank=True, null=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('bodega', models.IntegerField(blank=True, null=True)),
                ('clase_operacion', models.CharField(blank=True, max_length=10, null=True)),
                ('operacion', models.CharField(blank=True, max_length=100, null=True)),
                ('cantidad', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('valor_unidad', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('tiempo', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('porcentaje_iva', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('porcentaje_descuento', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('nit', models.CharField(blank=True, max_length=50, null=True)),
                ('nombres', models.CharField(blank=True, max_length=150, null=True)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('telefono_1', models.CharField(blank=True, max_length=50, null=True)),
                ('serie', models.CharField(blank=True, max_length=50, null=True)),
                ('modelo', models.CharField(blank=True, max_length=20, null=True)),
                ('placa', models.CharField(blank=True, max_length=50, null=True)),
                ('nombre_vendedor', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion_mo', models.CharField(blank=True, max_length=150, null=True)),
                ('descripcion_ref', models.CharField(blank=True, max_length=150, null=True)),
                ('vehiculo', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'v_interfaz_dms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VOperacionesAsesorAlt',
            fields=[
                ('no_orden', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('placas', models.CharField(blank=True, max_length=10, null=True)),
                ('vin', models.CharField(blank=True, max_length=50, null=True)),
                ('vehiculo', models.CharField(blank=True, max_length=250, null=True)),
                ('asesor', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'v_operaciones_asesor_alt',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VOperacionesRefacciones',
            fields=[
                ('fecha_ingreso', models.DateField(blank=True, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=25, primary_key=True, serialize=False)),
                ('placas', models.CharField(blank=True, max_length=10, null=True)),
                ('vin', models.CharField(blank=True, max_length=50, null=True)),
                ('vehiculo', models.CharField(blank=True, max_length=250, null=True)),
                ('asesor', models.CharField(blank=True, max_length=150, null=True)),
                ('tecnico', models.CharField(blank=True, max_length=60, null=True)),
                ('fin_tecnico', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'v_operaciones_refacciones',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VOperacionesTecnico',
            fields=[
                ('id', models.BigIntegerField(blank=True, primary_key=True, serialize=False)),
                ('id_hd', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('vin', models.CharField(blank=True, max_length=50, null=True)),
                ('placas', models.CharField(blank=True, max_length=10, null=True)),
                ('tecnico', models.CharField(blank=True, max_length=60, null=True)),
                ('asesor', models.CharField(blank=True, max_length=150, null=True)),
                ('vehiculo', models.CharField(blank=True, max_length=250, null=True)),
                ('fecha_llegada', models.DateField(blank=True, null=True)),
                ('hora_promesa', models.DateTimeField(blank=True, null=True)),
                ('cliente', models.CharField(blank=True, max_length=200, null=True)),
                ('servicio_capturado', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'v_operaciones_tecnico',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VSeguimientoEvidencia',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
                ('tecnico', models.CharField(blank=True, max_length=50, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('id_item', models.CharField(blank=True, max_length=50, null=True)),
                ('item', models.CharField(blank=True, max_length=250, null=True)),
                ('estado', models.CharField(blank=True, max_length=25, null=True)),
                ('comentarios', models.CharField(blank=True, max_length=500, null=True)),
                ('fecha_hora_inicio', models.DateTimeField(blank=True, null=True)),
                ('fecha_hora_fin', models.DateTimeField(blank=True, null=True)),
                ('fecha_hora_actualizacion', models.DateTimeField(blank=True, null=True)),
                ('no_cotizacion', models.CharField(blank=True, max_length=20, null=True)),
                ('valor', models.CharField(blank=True, max_length=50, null=True)),
                ('cambiado', models.BooleanField(blank=True, null=True)),
                ('evidencia', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'v_seguimiento_evidencia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VTecnicos',
            fields=[
                ('id_empleado', models.CharField(db_column='ID_EMPLEADO', max_length=10, primary_key=True, serialize=False)),
                ('id_tipo_empleado', models.CharField(blank=True, db_column='ID_TIPO_EMPLEADO', max_length=10, null=True)),
                ('nombre_empleado', models.CharField(blank=True, db_column='NOMBRE_EMPLEADO', max_length=60, null=True)),
                ('nivel', models.CharField(blank=True, db_column='NIVEL', max_length=1, null=True)),
                ('bahia', models.IntegerField(blank=True, db_column='BAHIA', null=True)),
                ('express', models.BooleanField(blank=True, db_column='EXPRESS', null=True)),
                ('color_tecnico', models.CharField(blank=True, db_column='COLOR_TECNICO', max_length=25, null=True)),
                ('hora_ent_lv', models.CharField(blank=True, db_column='HORA_ENT_LV', max_length=5, null=True)),
                ('hora_sal_lv', models.CharField(blank=True, db_column='HORA_SAL_LV', max_length=5, null=True)),
                ('hora_comer', models.CharField(blank=True, db_column='HORA_COMER', max_length=5, null=True)),
                ('hora_ent_s', models.CharField(blank=True, db_column='HORA_ENT_S', max_length=5, null=True)),
                ('hora_sal_s', models.CharField(blank=True, db_column='HORA_SAL_S', max_length=5, null=True)),
                ('id_asesor', models.CharField(blank=True, db_column='ID_ASESOR', max_length=10, null=True)),
                ('nombre_asesor', models.CharField(blank=True, db_column='NOMBRE_ASESOR', max_length=50, null=True)),
                ('no_emp_asesor', models.IntegerField(blank=True, db_column='NO_EMP_ASESOR', null=True)),
                ('jefe_taller', models.BooleanField(blank=True, db_column='JEFE_TALLER', null=True)),
                ('hora_ent_d', models.CharField(blank=True, db_column='HORA_ENT_D', max_length=5, null=True)),
                ('hora_sal_d', models.CharField(blank=True, db_column='HORA_SAL_D', max_length=5, null=True)),
                ('hora_comer_s', models.CharField(blank=True, db_column='HORA_COMER_S', max_length=5, null=True)),
                ('hora_comer_d', models.CharField(blank=True, db_column='HORA_COMER_D', max_length=5, null=True)),
                ('id_empleado_bi', models.CharField(blank=True, db_column='ID_EMPLEADO_BI', max_length=10, null=True)),
                ('min_comer_lv', models.IntegerField(blank=True, db_column='MIN_COMER_LV', null=True)),
                ('min_comer_s', models.IntegerField(blank=True, db_column='MIN_COMER_S', null=True)),
                ('min_comer_d', models.IntegerField(blank=True, db_column='MIN_COMER_D', null=True)),
            ],
            options={
                'db_table': 'v_tecnicos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VUsuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cvegrupo', models.IntegerField(db_column='cveGrupo')),
                ('cveperfil', models.IntegerField(db_column='cvePerfil')),
                ('cveusuario', models.CharField(db_column='cveUsuario', max_length=15)),
                ('pass_field', models.CharField(db_column='Pass', max_length=100)),
                ('nombre', models.CharField(blank=True, db_column='Nombre', max_length=150, null=True)),
                ('correoe', models.CharField(blank=True, db_column='correoE', max_length=100, null=True)),
                ('color', models.CharField(blank=True, db_column='Color', max_length=50, null=True)),
                ('cveasesor', models.CharField(blank=True, db_column='cveAsesor', max_length=20, null=True)),
            ],
            options={
                'db_table': 'v_usuarios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ActividadesAsesorFirmas',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_hd', models.CharField(blank=True, max_length=50, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=50, null=True)),
                ('firma', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_hora_fin', models.DateTimeField(auto_now_add=True)),
                ('fecha_hora_actualizacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'actividades_asesor_firmas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ActividadesCalidad',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('item', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'actividades_calidad',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ActividadesTecnicoCaptura',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('no_orden', models.CharField(blank=True, max_length=10, null=True)),
                ('item', models.CharField(blank=True, max_length=100, null=True)),
                ('valor', models.CharField(blank=True, max_length=300, null=True)),
                ('fecha_hora_fin', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'actividades_tecnico_captura',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistorialEvidencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.ImageField(upload_to='')),
                ('hora_subida', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'historial_evidencias',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Informacion',
            fields=[
                ('no_orden', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('vin', models.CharField(blank=True, max_length=30, null=True)),
                ('kilometraje', models.CharField(blank=True, max_length=20, null=True)),
                ('asesor', models.CharField(blank=True, max_length=100, null=True)),
                ('cliente', models.CharField(blank=True, max_length=500, null=True)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=150, null=True)),
                ('placas', models.CharField(blank=True, max_length=10, null=True)),
                ('vehiculo', models.CharField(blank=True, max_length=100, null=True)),
                ('modelo', models.CharField(blank=True, max_length=120, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_hora_ingreso', models.DateTimeField(blank=True, null=True)),
                ('tecnico', models.CharField(blank=True, max_length=250, null=True)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'informacion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('estado', models.CharField(blank=True, max_length=25, null=True)),
                ('comentarios', models.CharField(blank=True, max_length=500, null=True)),
                ('valor', models.CharField(blank=True, max_length=50, null=True)),
                ('bateria_estado', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True)),
                ('bateria_nivel', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True)),
                ('cambiado', models.BooleanField(default=0)),
                ('tecnico', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_hora_fin', models.DateTimeField(auto_now_add=True)),
                ('fecha_hora_actualizacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'actividades_tecnico',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ListaItemsTecnicoCaptura',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=400, null=True)),
                ('x', models.IntegerField(blank=True, null=True)),
                ('y', models.IntegerField(blank=True, null=True)),
                ('size', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('line_size', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lista_items_tecnico_captura',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LogCliente',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('cliente', models.BinaryField(blank=True, max_length='max', null=True)),
                ('fecha_hora_visita', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'log_cliente',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LogEnvios',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('medio', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_hora_envio', models.DateTimeField(blank=True, null=True)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('correo', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'log_envios',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LogGeneral',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('inicio_tecnico', models.DateTimeField(blank=True, null=True)),
                ('fin_tecnico', models.DateTimeField(blank=True, null=True)),
                ('inicio_refacciones', models.DateTimeField(blank=True, null=True)),
                ('fin_refacciones', models.DateTimeField(blank=True, null=True)),
                ('inicio_mano_de_obra', models.DateTimeField(blank=True, null=True)),
                ('fin_mano_de_obra', models.DateTimeField(blank=True, null=True)),
                ('inicio_asesor', models.DateTimeField(blank=True, null=True)),
                ('fin_asesor', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'log_general',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Revisiones',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=150, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'lista_revisiones',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TiposCargos',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'lista_tipos_cargos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TiposCotizacion',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'lista_tipos_cotizacion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TiposRefacciones',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'lista_tipos_refacciones',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Refacciones',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=50, null=True)),
                ('nombre', models.CharField(blank=True, max_length=250, null=True)),
                ('no_parte', models.CharField(blank=True, max_length=50, null=True)),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('precio_unitario', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('porcentaje_descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('porcentaje_iva', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('subtotal_iva', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('existencia', models.CharField(blank=True, max_length=10, null=True)),
                ('localizacion', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_hora_fin', models.DateTimeField(auto_now_add=True)),
                ('fecha_hora_actualizacion', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.items')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.tiposrefacciones')),
            ],
            options={
                'db_table': 'actividades_refacciones',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ManoDeObra',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=50, null=True)),
                ('codigo', models.CharField(blank=True, max_length=50, null=True)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('cantidad_uts', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('precio_ut', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('porcentaje_descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('porcentaje_iva', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('subtotal_iva', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('fecha_hora_fin', models.DateTimeField(auto_now_add=True)),
                ('fecha_hora_actualizacion', models.DateTimeField(auto_now=True)),
                ('cargo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.tiposcargos')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.items')),
            ],
            options={
                'db_table': 'actividades_mano_de_obra',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ListaItems',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('orden', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('familia', models.CharField(blank=True, max_length=250, null=True)),
                ('multipuntos', models.BooleanField(blank=True, null=True)),
                ('pagina', models.IntegerField(blank=True, null=True)),
                ('g_x', models.IntegerField(blank=True, null=True)),
                ('g_y', models.IntegerField(blank=True, null=True)),
                ('y_x', models.IntegerField(blank=True, null=True)),
                ('y_y', models.IntegerField(blank=True, null=True)),
                ('r_x', models.IntegerField(blank=True, null=True)),
                ('r_y', models.IntegerField(blank=True, null=True)),
                ('modificado_x', models.IntegerField(blank=True, null=True)),
                ('modificado_y', models.IntegerField(blank=True, null=True)),
                ('valor_x', models.IntegerField(blank=True, null=True)),
                ('valor_y', models.IntegerField(blank=True, null=True)),
                ('revision', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.revisiones')),
            ],
            options={
                'db_table': 'lista_items_tecnico',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='items',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.listaitems'),
        ),
        migrations.CreateModel(
            name='Evidencias',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('evidencia', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_hora_fin', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.items')),
            ],
            options={
                'db_table': 'actividades_tecnico_medios',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CotizacionPdf',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=500, null=True)),
                ('fecha_hora_fin', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.tiposcotizacion')),
            ],
            options={
                'db_table': 'actividades_cotizacion_pdf',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Autorizaciones',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_hd', models.BigIntegerField(blank=True, null=True)),
                ('no_orden', models.CharField(blank=True, max_length=25, null=True)),
                ('autorizacion', models.BooleanField(default=0)),
                ('pagado', models.BooleanField(default=0)),
                ('fecha_hora_fin', models.DateTimeField(auto_now_add=True)),
                ('fecha_hora_actualizacion', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguimientolite_mazda_col.items')),
            ],
            options={
                'db_table': 'actividades_cliente',
                'managed': True,
            },
        ),
    ]
