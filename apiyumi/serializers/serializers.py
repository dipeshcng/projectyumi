from ..models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from ..utils.validators import *
from apiyumi.utils.utils import calculate_age


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


#Business classes serializer 
class BusinessRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True, style= {'input_type':'password'})
    class Meta:
        model = BusinessDetail
        fields = ['name_of_business', 'business_logo', 'business_contact', 
                  'location', 'start_date',
                    'end_date', 'email', 'password']
        
    def create(self, validated_data):
        role_instance, created = Role.objects.get_or_create(role_type = 'host business')
        if created:
            # Set other attributes for the newly created role if needed
            role_instance.status = 'Active'
            role_instance.save()
        email = validate_email(validated_data['email'])
        password = validate_password(validated_data['password'])
        name_of_business = validated_data['name_of_business']
        business_logo = validated_data.get('business_logo')
        business_contact = validated_data['business_contact']
        location = validated_data['location']
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        bus = BusinessDetail.objects.create(name_of_business=name_of_business,business_contact=business_contact,location=location,
                                        start_date=start_date, end_date=end_date, role=role_instance, business_logo=business_logo)
        user = User.objects.create_user(username=email, email=email)
        user.set_password(password)
        user.save()
        bus.user = user
        bus.save()
        return validated_data
    
    def get_business_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.business_logo.url)

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetail
        fields = ['id', 'name_of_business', 'business_contact', 'location', 'business_logo']
        read_fields = ['id', 'name_of_business', ]

        def update(self, instance, validated_data):
            instance.name_of_business = validated_data.get('name_of_business', instance.name_of_business)
            instance.business_logo = validated_data.get('business_logo', instance.business_logo)
            instance.save()
            return instance
    
        def get_business_logo(self, obj):
            return self.context['request'].build_absolute_uri(obj.business_logo.url)



#Graduate classes serializers
class GraduateRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True, style= {'input_type':'password'})
    
    class Meta:
        model = GraduatesDetail
        fields = ["full_name", "dob", "email", "password", "phone", "image"]

    def create(self, validated_data):
        role_instance, created = Role.objects.get_or_create(role_type = 'graduate')
        if created:
            # Set other attributes for the newly created role if needed
            role_instance.status = 'Active'
            role_instance.save()
        email = validate_email(validated_data['email'])
        password = validate_password(validated_data['password'])
        full_name = validated_data['full_name']
        dob = validated_data["dob"]
        age = calculate_age(dob)
        phone = validated_data['phone']
        image = validated_data['image']
        grad = GraduatesDetail.objects.create(full_name=full_name, dob=dob, phone=phone, image=image, role=role_instance)
        usr = User.objects.create_user(username=email, email=email)
        usr.set_password(password)
        usr.save()
        grad.user = usr
        grad.save()
        return validated_data
    

class Graduateprofileserializer(serializers.ModelSerializer):

    class Meta:
        model = GraduatesDetail
        fields = ['id', 'full_name', 'dob', 'image', 'phone']
        read_only_fields = ['id', 'dob']

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)




#volunteer serializer
class VolunteerRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True, style= {'input_type':'password'})

    class Meta:
        model = Volunteer
        fields = ['id','email', 'password', 'full_name', 'image']
    
    def create(self, validated_data):
        role_instance, created = Role.objects.get_or_create(role_type = 'volunteer')
        if created:
            # Set other attributes for the newly created role if needed
            role_instance.status = 'Active'
            role_instance.save()
        email = validate_email(validated_data['email'])
        password = validate_password(validated_data['password'])
        full_name = validated_data['full_name']
        image = validated_data.get('image', None)
        volt = Volunteer.objects.create(role=role_instance, full_name = full_name, image=image)
        usr = User.objects.create_user(username=email, email=email)
        usr.set_password(password)
        usr.save()
        volt.user = usr
        volt.save()
        return validated_data
    

class Volunteerprofileserializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['id', 'full_name','image']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    
    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)