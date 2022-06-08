import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from accounts.utils import get_admin_perm


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_perm = get_admin_perm()

        username = os.getenv("DEFAULT_ADMIN_USERNAME")
        password = os.getenv("DEFAULT_ADMIN_USERNAME")
        if not User.objects.filter(username=username).exists():
            admin_user = User.objects.create(
                username=username
            )
            admin_user.set_password(password)
            admin_user.user_permissions.add(admin_perm)
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            return
        print("**User already exists**")
