from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from .validators import *

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


#Business classes serializer 
class BusinessRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True, style= {'input_type':'password'})
    class Meta:
        model = BusinessDetail
        fields = ['name_of_business', 'business_contact', 
                  'location', 'number_of_employee', 'number_of_new_hires', 'level_of_recruitment',
                  'salary', 'start_date', 'end_date', 'email', 'password']
        
    def create(self, validated_data):
        email = validate_email(validated_data['email'])
        password = validate_password(validated_data['password'])
        name_of_business = validated_data['name_of_business']
        business_contact = validated_data['business_contact']
        location = validated_data['location']
        number_of_employee = validated_data['number_of_employee']
        number_of_new_hires = validated_data['number_of_new_hires']
        level_of_recruitment = validated_data['level_of_recruitment']
        salary = validated_data['salary']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        bus = BusinessDetail.objects.create(name_of_business=name_of_business,business_contact=business_contact,location=location,
                                       number_of_employee=number_of_employee, number_of_new_hires=number_of_new_hires, level_of_recruitment=level_of_recruitment,
                                       salary=salary, start_date=start_date, end_date=end_date)
        user = User.objects.create_user(username=email, email=email)
        user.set_password(password)
        user.save()
        bus.user = user
        bus.save()
        return validated_data


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetail
        fields = "__all__"



#Graduate classes serializers
class GraduateRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True, style= {'input_type':'password'})
    class Meta:
        model = GraduatesDetail
        fields = ["full_name", "dob", "email", "password", "phone", "image"]

    def create(self, validated_data):
        email = validate_email(validated_data['email'])
        password = validate_password(validated_data['password'])
        full_name = validated_data['full_name']
        dob = validated_data["dob"]
        phone = validated_data['phone']
        image = validated_data['image']
        grad = GraduatesDetail.objects.create(full_name=full_name, dob=dob, phone=phone, image=image)
        usr = User.objects.create_user(username=email, email=email)
        usr.set_password(password)
        usr.save()
        grad.user = usr
        grad.save()
        return validated_data
    

class Graduateprofileserializer(serializers.ModelSerializer):
    class Meta:
        model = GraduatesDetail
        fields = "__all__"