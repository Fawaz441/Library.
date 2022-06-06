from django.urls import path
from .views import (LoginView, AddUser, DeleteManager,
                    StudentListAPIView, ManagerListAPIView,
                    SignupView, StudentSuspendAPIView, StudentUnSuspendAPIView)

urlpatterns = [
    path('login', LoginView.as_view()),
    path('add-user', AddUser().as_view()),
    path('delete-manager', DeleteManager.as_view()),
    path('students', StudentListAPIView.as_view()),
    path('managers', ManagerListAPIView.as_view()),
    path('student/sign-up', SignupView.as_view()),
    path('student/<str:username>/suspend', StudentSuspendAPIView.as_view()),
    path('student/<str:username>/unsuspend',
         StudentUnSuspendAPIView.as_view()),
]
