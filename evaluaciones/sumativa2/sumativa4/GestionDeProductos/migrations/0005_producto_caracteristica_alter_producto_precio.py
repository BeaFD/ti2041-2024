# Generated by Django 5.1.1 on 2024-10-21 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeProductos', '0004_remove_producto_caracteristica'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='caracteristica',
            field=models.ManyToManyField(to='GestionDeProductos.caracteristica'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.IntegerField(),
        ),
    ]
