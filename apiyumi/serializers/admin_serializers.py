from rest_framework import serializers
from apiyumi.models import Admin, Role
from django.contrib.auth.models import User
from ..utils.validators import validate_email, validate_password

class AdminRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True, style= {'input_type':'password'})

    class Meta:
        model = Admin
        fields = ['email', 'password', 'full_name']

    def create(self, validated_data):
        role = Role.objects.get(role_type = 'admin')
        email = validate_email(validated_data['email'])
        password = validate_password(validated_data['password'])
        full_name = validated_data['full_name']
        admin = Admin.objects.create(role=role, full_name=full_name)
        usr = User.objects.create_user(username=email, email=email)
        usr.set_password(password)
        usr.save()
        admin.user = usr
        admin.save()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class AdminProfileserialzer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Admin
        fields = ['user', 'full_name']