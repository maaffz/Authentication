from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from .models import User

class ChangePasswordSerializer(serializers.Serializer):
    model=User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)