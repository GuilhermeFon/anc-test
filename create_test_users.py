#!/usr/bin/env python
"""Script para criar usuários padrão do sistema."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Usuario

admin, created = Usuario.objects.get_or_create(
    username='admin',
    defaults={'is_staff': True, 'is_superuser': True}
)
admin.set_password('admin123')
admin.is_staff = True
admin.is_superuser = True
admin.save()

status_admin = 'criado' if created else 'atualizado'
print(f'✓ Admin {status_admin}: admin/admin123 (Cartório)')

produtor, created = Usuario.objects.get_or_create(
    username='produtor',
    defaults={'is_staff': False}
)
produtor.set_password('produtor123')
produtor.is_staff = False
produtor.save()

status_prod = 'criado' if created else 'atualizado'
print(f'✓ Produtor {status_prod}: produtor/produtor123 (Produtor)')
