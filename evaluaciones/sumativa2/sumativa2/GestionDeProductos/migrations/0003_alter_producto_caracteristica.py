# Generated by Django 5.1.1 on 2024-10-21 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeProductos', '0002_productocaracteristica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='caracteristica',
            field=models.ManyToManyField(through='GestionDeProductos.ProductoCaracteristica', to='GestionDeProductos.caracteristica'),
        ),
    ]