import django
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeProductos', '0008_merge_0006_auto_20241118_1857_0007_auto_20241118_1859'),  # Replace with your actual dependency
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoCaracteristica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=100)),
                ('caracteristica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionDeProductos.Caracteristica')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionDeProductos.Producto')),
            ],
        ),
    ]