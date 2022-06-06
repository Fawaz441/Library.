from django.contrib.auth.models import Group, Permission, User, ContentType
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError

ADMIN = "ADMIN"
STUDENT = "STUDENT"
MANAGER = "MANAGER"
MANAGER_CODENAME = 'can_manage_books'
STUDENT_CODENAME = 'can_borrow_and_return_books'
ADMIN_CODENAME = 'can_create_and_delete_managers'


def get_perm(name, codename):
    ct = ContentType.objects.get_for_model(User)
    return Permission.objects.get_or_create(codename=codename,
                                            name=name,
                                            content_type=ct)[0]


def get_manager_perm():
    return get_perm(MANAGER, MANAGER_CODENAME)


def get_student_perm():
    return get_perm(STUDENT, STUDENT_CODENAME)


def get_admin_perm():
    return get_perm(ADMIN, ADMIN_CODENAME)


def is_manager(user):
    return user.has_perm('auth.{0}'.format(MANAGER_CODENAME))


def is_admin(user):
    return user.has_perm('auth.{0}'.format(ADMIN_CODENAME))


def is_student(user):
    return user.has_perm('auth.{0}'.format(STUDENT_CODENAME))


def is_strong_password(user, password):
    password_errors = []
    validators = get_default_password_validators()
    for validator in validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            password_errors.append(error)
    return password_errors
