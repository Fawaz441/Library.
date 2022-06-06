from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.utils import get_admin_perm

class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_perm = get_admin_perm()

        username = 'admin'
        password = 'adminpassword10'

        admin_user = User.objects.create(
            username = username
        )
        admin_user.set_password(password)
        admin_user.user_permissions.add(admin_perm)
        admin_user.save()
        
