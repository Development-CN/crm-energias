# Generated by Django 4.2.4 on 2024-08-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboards", "0014_alter_historial_operacion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historial",
            name="operacion",
            field=models.CharField(max_length=3000, null=True),
        ),
    ]