from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from GestionDeProductos.models import Producto

class Command(BaseCommand):
    help = 'Create user groups and permissions'

    def handle(self, *args, **kwargs):
        # Create group
        admin_products_group, created = Group.objects.get_or_create(name='ADMIN_PRODUCTS')

        # Define permissions
        permissions = [
            'add_producto',
            'change_producto',
            'delete_producto',
            'view_producto',
        ]

        # Assign permissions to group
        content_type = ContentType.objects.get_for_model(Producto)
        for perm in permissions:
            permission, created = Permission.objects.get_or_create(codename=perm, content_type=content_type)
            admin_products_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully created user groups and permissions'))