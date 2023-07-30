from django.contrib.auth.models import User
from rest_framework import serializers

def validate_email(email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("email already exists")
        return email
    

def validate_password(value):
    if value.isalnum():
        raise serializers.ValidationError('password must have atleast one special character.')
    return value


def validate_graduate_age(value):
    if value < 16:
        raise serializers.ValidationError('graduate must be above 16 years old')
    return value