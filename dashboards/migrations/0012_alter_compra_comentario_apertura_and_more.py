# Generated by Django 4.2.4 on 2024-08-27 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboards", "0011_asesor_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="compra",
            name="comentario_apertura",
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="historial",
            name="comentarios",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="lead",
            name="comentario",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="log",
            name="comentarios",
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="vehiculosintereslead",
            name="comentario",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
