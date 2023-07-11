from django.contrib.auth.models import User
from rest_framework import serializers

def validate_email(email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email":"email already exists"})
        return email
    

def validate_password(value):
    if value.isalnum():
        raise serializers.ValidationError('password must have atleast one special character.')
    return value