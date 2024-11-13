# Generated by Django 4.2.7 on 2024-09-28 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0016_catalogomodelo_years'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='cilindros',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='kit_conversion',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='tipo_inyeccion',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='tipo',
            field=models.CharField(choices=[('Llamada cliente', 'Llamada cliente'), ('Mensaje cliente', 'Mensaje cliente'), ('Visita cliente', 'Visita cliente'), ('Recepción del cliente', 'Recepción del cliente'), ('Envio de propuesta economica', 'Envio de propuesta economica'), ('Contacto proximo servicio', 'Contacto proximo servicio')], max_length=255, null=True),
        ),
    ]