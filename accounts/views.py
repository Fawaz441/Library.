from django.contrib.auth import login
from django.contrib.auth.password_validation import get_default_password_validators
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from utils.response import error_response, success_response

from accounts.utils import(
    ADMIN, MANAGER, get_admin_perm, get_manager_perm, is_manager, is_student,
    get_student_perm, is_strong_password)
from .permissions import IsAdmin, IsManager
from .serializers import (CreateUserSerializer, LoginSerializer,
                          DeleteManagerSerializer, StudentSerializer,
                          ManagerSerializer, StudentSignupSerializer)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = LoginSerializer(data=request.POST)
        if data.is_valid():
            data = data.validated_data
            username = data.get('username')
            password = data.get('password')
            user = User.objects.filter(username=username).first()
            if not user:
                return error_response(error='Invalid credentials')
            if not user.is_active:
                print(user.user_permissions.all())
                for perm in user.user_permissions.all():
                    print(perm.codename)
                print('reached here')
                return error_response(error="You have been suspended")
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return success_response(data=tokens)
            return error_response(error='Invalid credentials')
        return error_response(error=data.errors)


class SignupView(APIView):

    def post(self, request):
        data = StudentSignupSerializer(data=request.data)
        if data.is_valid():
            password = data.validated_data.pop('password')
            student = User(
                **data.validated_data
            )
            password_errors = is_strong_password(student, password)
            if password_errors:
                return error_response(error=password_errors)
            student.set_password(password)
            student.save()
            student.user_permissions.add(get_student_perm())
            return success_response(message="Successful sign up")
        return error_response(error=data.errors)
    # admin views


class AddUser(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        print(request.user)
        data = CreateUserSerializer(data=request.POST)
        if data.is_valid():
            data = data.validated_data
            username = data.get('username')
            password = data.get('password')
            type = data.get('type')
            temp_user = User(username=username)
            validators = get_default_password_validators()
            password_errors = is_strong_password(temp_user, password)
            if password_errors:
                return error_response(error=password_errors)
            temp_user.set_password(password)
            temp_user.save()
            if type == ADMIN:
                temp_user.user_permissions.add(get_admin_perm())
            if type == MANAGER:
                temp_user.user_permissions.add(get_manager_perm())
            message = '{0} created successfully'.format(type)
            return success_response(message=message)
        return error_response(error=data.errors)


class DeleteManager(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        data = DeleteManagerSerializer(data=request.data)
        if data.is_valid():
            user = data.validated_data.get('username')
            if not is_manager(user):
                return error_response(error="User is not a manager")
            else:
                user.delete()
                return success_response(message="Manager deleted successfully")
        else:
            return error_response(error=data.errors)


class StudentListAPIView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        status = request.GET.get('status')
        students = User.objects.filter(user_permissions=get_student_perm())
        if status == 'suspended':
            students = students.filter(is_active=False)
        if status == 'unsuspended':
            students = students.filter(is_active=True)
        data = StudentSerializer(students, many=True).data
        return success_response(data=data)


class ManagerListAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        managers = User.objects.filter(user_permissions=get_manager_perm())
        data = ManagerSerializer(managers, many=True).data
        return success_response(data=data)


class StudentSuspendAPIView(APIView):
    permission_classes = [IsManager]

    def post(self, request, username):
        student = User.objects.filter(
            user_permissions=get_student_perm(), username=username).first()
        if not student:
            return error_response(error="Student does not exist")
        if not student.is_active:
            return error_response(error="{} has already been suspended".format(student.username))
        student.is_active = False
        student.save()
        return success_response(message="{} has been suspended successfully".format(student.username))


class StudentUnSuspendAPIView(APIView):
    permission_classes = [IsManager]

    def post(self, request, username):
        student = User.objects.filter(
            user_permissions=get_student_perm(), username=username).first()
        if not student:
            return error_response(error="Student does not exist")
        if student.is_active:
            return error_response(error="{} is not suspended".format(student.username))
        student.is_active = True
        student.save()
        return success_response(message="{} has been unsuspended successfully".format(student.username))
