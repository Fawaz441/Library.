from django.contrib.auth.models import User
from rest_framework.serializers import Serializer, BooleanField, CharField, ValidationError, ModelSerializer, SerializerMethodField
from accounts.utils import ADMIN, MANAGER


class LoginSerializer(Serializer):
    username = CharField()
    password = CharField()


class StudentSignupSerializer(ModelSerializer):
    password = CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        extra_kwargs = {'first_name': {'required': True,
                                       'allow_blank': False}, 'last_name': {'required': True,
                                                                            'allow_blank': False}}


class CreateUserSerializer(Serializer):
    username = CharField()
    password = CharField()
    type = CharField()

    def validate_username(self, username):
        if User.objects.filter(username__iexact=username):
            raise ValidationError("A user already has this username")
        return username

    def validate_type(self, type):
        if type in [ADMIN, MANAGER]:
            return type
        raise ValidationError(
            "Type must be either {0} or {1}".format(ADMIN, MANAGER))


class DeleteManagerSerializer(Serializer):
    username = CharField()

    def validate_username(self, username):
        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(
                "This user does not exist. Please note that the username is case-sensitive")
        return user


class ManagerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'date_joined', 'last_login']


class StudentSerializer(ModelSerializer):
    is_suspended = SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'date_joined',
                  'last_login', 'is_suspended']

    def get_is_suspended(self, user):
        return not user.is_active
