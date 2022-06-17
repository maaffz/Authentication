from django.contrib import admin
from django.urls import path
from .views import userlogin, create,ChangePasswordView

urlpatterns = [
    path('user/login/', userlogin),
    path('user/create/', create),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]