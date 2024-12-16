from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeProductos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='caracteristica',
        ),
    ]