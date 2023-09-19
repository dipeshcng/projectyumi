from rest_framework import serializers
from apiyumi.models import Admin, Role, BusinessDetail, Volunteer, GraduatesDetail
from django.contrib.auth.models import User
from ..utils.validators import validate_email, validate_password

class AdminRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True, style= {'input_type':'password'})

    class Meta:
        model = Admin
        fields = ['email', 'password', 'full_name']

    def create(self, validated_data):
        role_instance, created = Role.objects.get_or_create(role_type = 'admin')
        if created:
            # Set other attributes for the newly created role if needed
            role_instance.status = 'Active'
            role_instance.save()
        email = validate_email(validated_data['email'])
        password = validate_password(validated_data['password'])
        full_name = validated_data['full_name']
        admin = Admin.objects.create(role=role_instance, full_name=full_name)
        usr = User.objects.create_user(username=email, email=email, first_name=full_name)
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

#Business
class BusinessProfileForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetail
        fields = ['id', 'status', 'name_of_business', 'business_contact', 'location', 'business_logo', 'created_at']
        read_only_fields = ['id', 'name_of_business', 'business_logo', 'created_at']

        def update(self, instance, validated_data):
            instance.business_contact = validated_data.get('business_contact', instance.business_contact)
            instance.location = validated_data.get('location', instance.location)
            instance.status = validated_data.get('status', instance.status)
            instance.save()
            return instance
    
        def get_business_logo(self, obj):
            return self.context['request'].build_absolute_uri(obj.business_logo.url)

#Graduate
class GraduateDetailForAdminserializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = GraduatesDetail
        fields = ['id', 'status',  'email', 'full_name', 'dob', 'image', 'phone', 'created_at', 'working_status']
        read_only_fields = ['id', 'dob', 'created_at', 'email']

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


#Volunteer
class VolunteerDetailForAdminserializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['id', 'status', 'full_name','image', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)