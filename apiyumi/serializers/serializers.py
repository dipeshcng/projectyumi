from ..models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from ..utils.validators import *
from apiyumi.utils.utils import calculate_age
from apiyumi.utils.utils import convert_date
from datetime import datetime, date


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    roles = serializers.ListField()

    def to_representation(self, instance):
        return {
            'email': instance.email,
        }

        
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
        if start_date is None:
            start_date = date.today()
        end_date = validated_data.get('end_date')
        bus = BusinessDetail.objects.create(name_of_business=name_of_business,business_contact=business_contact,location=location,
                                        start_date=start_date, end_date=end_date, role=role_instance, business_logo=business_logo)
        user = User.objects.create_user(username=email, email=email, first_name=name_of_business)
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
        fields = ['id', 'name_of_business', 'business_contact', 'location', 'business_logo', 'created_at']
        read_only_fields = ['id', 'name_of_business', 'business_logo', 'created_at']

        def update(self, instance, validated_data):
            instance.business_contact = validated_data.get('business_contact', instance.business_contact)
            instance.location = validated_data.get('location', instance.location)
            instance.save()
            return instance
    
        def get_business_logo(self, obj):
            return self.context['request'].build_absolute_uri(obj.business_logo.url)




#Graduate classes serializers
class GraduateRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True, style= {'input_type':'password'})
    # resume = serializers.FileField()
    class Meta:
        model = GraduatesDetail
        fields = ["full_name", "dob", "email", "password", "phone", "working_status"]

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
        working_status = validated_data.get('working_status')
        if working_status is None:
            working_status = "Looking for job"
        # age = calculate_age(dob)
        phone = validated_data['phone']
        # image = validated_data['image']
        resume = validated_data.get('resume', None)
        grad = GraduatesDetail.objects.create(full_name=full_name, dob=dob, phone=phone, role=role_instance, working_status=working_status)
        usr = User.objects.create_user(username=email, email=email, first_name=full_name)
        usr.set_password(password)
        usr.save()
        grad.user = usr
        grad.save()
        if resume is not None:
            resume = Resume.objects.create(user=grad, resume=resume)
        return validated_data
    
class ResumeListForGraduateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('id', 'resume')
    
    def get_resume(self, obj):
        return self.context['request'].build_absolute_uri(obj.resume.url)

class Graduateprofileserializer(serializers.ModelSerializer):
    resume_list = ResumeListForGraduateSerializer(many=True, read_only=True)
    class Meta:
        model = GraduatesDetail
        fields = ['id','user' ,'full_name', 'dob', 'image', 'phone', "working_status", "resume_list"]
        read_only_fields = ['id', 'dob', 'resume_list']

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
    



class ResumeSerializer(serializers.ModelSerializer):
    graduate = Graduateprofileserializer(read_only=True, source='user')
    class Meta:
        model = Resume
        fields = [ 'graduate', 'resume']

    def get_resume(self, obj):
        return self.context['request'].build_absolute_uri(obj.resume.url)
    
    

# serializers.py

class ResumeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('id', 'title', 'resume')
    
    def get_resume(self, obj):
        return self.context['request'].build_absolute_uri(obj.resume.url)

class GraduatesDetailSerializer(serializers.ModelSerializer):
    resume_set = ResumeListSerializer(many=True, read_only=True)
    email = serializers.EmailField(source="user.username")
    role = serializers.CharField(source='role.role_type')

    class Meta:
        model = GraduatesDetail
        fields = ('id', 'working_status' ,'email', 'role', 'full_name', 'dob', 'image', 'phone', 'resume_set')
    
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
        usr = User.objects.create_user(username=email, email=email, first_name=full_name)
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
    
#Events serializers
class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_name', 'location', 'description', 'document','event_start_date', 'event_end_date']
    def create(self, validated_data):
        event_name = validated_data['event_name']
        location = validated_data['location']
        description = validated_data['description']
        document = validated_data.get('document')
        event_start_date = validated_data['event_start_date']
        event_end_date = validated_data['event_end_date']
        user = self.context['request'].user
        Event.objects.create(posted_by=user, event_name=event_name, location=location, description=description, event_start_date=event_start_date, 
                                     document=document,event_end_date=event_end_date, status='Active')
        return validated_data

    def update(self, instance, validate_data):
        instance.event_name = validate_data.get('event_name', instance.event_name)
        instance.location = validate_data.get('location', instance.location)
        instance.description = validate_data.get('description', instance.description)
        instance.document = validate_data.get('document', instance.document)
        instance.event_start_date = validate_data.get('event_start_date', instance.event_start_date)
        instance.event_end_date = validate_data.get('event_end_date', instance.event_end_date)
        instance.save()
        return instance
    
    


class EventListSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','event_name','event_start_date', 'event_end_date']
    

class EventDetailSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','event_name', 'location', 'description', 'document', 'event_start_date', 'event_end_date']
    
    def get_document(self, obj):
        return self.context['request'].build_absolute_uri(obj.document.url)

class RegisteredBySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'full_name']
    
    def get_full_name(self, obj):
        if hasattr(obj, 'volunteer'):
            full_name = obj.volunteer.full_name
        elif hasattr(obj, 'graduate'):
            full_name = obj.graduate.full_name
        elif hasattr(obj, 'hostbusiness'):
            full_name = obj.hostbusiness.name_of_business
        else:
            full_name = None
        return full_name

class EventDetailForAdminSerialzer(serializers.ModelSerializer):
    registered_by = RegisteredBySerializer(read_only=True, many=True)
    class Meta:
        model = Event
        fields = ['id', 'event_name', 'location', 'description', 'document', 'event_start_date', 'event_end_date', 'registered_by']

    def get_document(self, obj):
        return self.context['request'].build_absolute_uri(obj.document.url)

    # def get_registered_by(self, obj):
    #     # Assuming that 'registered_by' is a ManyToMany field to the User model
    #     # You can use this method to get the emails of all users in the 'registered_by' field
    #     return [user.username for user in obj.registered_by.all()]
    
#job serializer
class JobCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['posted_by','title', 'salary_type', 'salary', 'no_of_hires', 'requirements', 'application_start_date',
                  'application_end_date', 'location', 'description']
        read_only_fields = ['posted_by']
        
    def create(self, validated_data):
        title = validated_data.get('title')
        salary_type = validated_data.get('salary_type')
        salary = validated_data.get('salary')
        no_of_hires = validated_data.get('no_of_hires')
        requirements = validated_data.get('requirements')
        application_start_date = validated_data.get('application_start_date')
        application_end_date = validated_data.get('application_end_date')
        location = validated_data.get('location')
        description = validated_data.get('description')
        user = self.context['request'].user
        Job.objects.create(posted_by=user, title=title, salary_type=salary_type, salary=salary, no_of_hires=no_of_hires, requirements=requirements,application_start_date=application_start_date,
                            application_end_date=application_end_date, location=location, description=description)
        return validated_data


class JobListDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = ['id','creator', 'title', 'salary_type', 'salary', 'no_of_hires', 'requirements', 'application_start_date',
                  'application_end_date', 'location', 'description']
        
    def get_description(self, obj):
        return self.context['request'].build_absolute_uri(obj.description.url)
    
    def get_creator(self, obj):
        if hasattr(obj.posted_by, 'hostbusiness'):
            creator_instance = obj.posted_by.hostbusiness.name_of_business
        else:
            creator_instance = "Project Yumi"

        if creator_instance:
            return creator_instance 
        
        return None


    

class ResumeHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['user', 'resume']

class JobMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMessage
        fields = ['user', 'message']

class JobListDetailForAdminSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField(read_only=True)
    applied_graduates = ResumeSerializer(read_only=True, many=True)
    message = JobMessageSerializer(read_only=True, many=True, source='jobmessage_set')

    class Meta:
        model = Job
        fields = ['id','posted_by', 'creator','title', 'salary_type', 'salary', 'no_of_hires', 'requirements', 'application_start_date',
                  'application_end_date', 'location', 'description', 'applied_graduates', 'message']
        
    def get_description(self, obj):
        return self.context['request'].build_absolute_uri(obj.description.url)
    
    def get_creator(self, obj):
        if hasattr(obj.posted_by, 'hostbusiness'):
            creator_instance = obj.posted_by.hostbusiness.name_of_business
        else:
            creator_instance = "Project Yumi"

        if creator_instance:
            return creator_instance 
        
        return None

# class JobAppliedResumeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Resume
#         fields = ['user', 'resume']
    
#     def get_resume(self, obj):
#         return self.context['request'].build_absolute_uri(obj.resume.url)


#resume
class ResumeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id','resume']
        read_only_fileds = ['id']
    
    def create(self, validated_data):
        resume = validated_data.get('resume')
        usr = self.context['request'].user.graduate
        Resume.objects.create(user = usr, resume=resume, status="Active")
        return validated_data
    
    def get_resume(self, obj):
        return self.context['request'].build_absolute_uri(obj.resume.url)
    

#Programs
class ProgramDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramDocument
        fields = ['id','document']
    
    def create(self, validated_data):
        documents = self.context['request'].FILES.getlist('document', [])
        program = self.context['program']
        for doc in documents:
            ProgramDocument.objects.create(status='Active',program=program, document=doc)
        return validated_data
    
    def get_document(self, obj):
        return self.context['request'].build_absolute_uri(obj.document.url)

class ProgramListSerializer(serializers.ModelSerializer):
    total_documents = serializers.SerializerMethodField()
    total_register = serializers.SerializerMethodField()
    class Meta:
        model = Program
        fields = ['id', "posted_by", 'title', 'location','description', 'start_date', 'end_date', 'total_slots', 'total_documents', 'total_register']
    
    def get_total_documents(self, obj):
        return obj.programdocument_set.count()
    
    def get_total_register(self, obj):
        return obj.registered_by.all().count()

class ProgramDetailSerializer(serializers.ModelSerializer):
    documents = ProgramDocumentSerializer(many=True, read_only=True,  source='programdocument_set')
    class Meta:
        model = Program
        fields = ['id', "posted_by", 'title', 'location','description', 'start_date', 'end_date', 'total_slots', 'documents']
        # read_only_fields = ['id', "posted_by"]

class ProgramSerializer(serializers.ModelSerializer):
    document = serializers.FileField()
    class Meta:
        model = Program
        fields = ['id', "posted_by", 'title', 'location','description', 'start_date', 'end_date', 'total_slots', 'document']
        read_only_fields = ['id', "posted_by"]

    def create(self, validated_data):
        title = validated_data['title']
        description = validated_data['description']
        location = validated_data['location']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        user = self.context['request'].user
        program = Program.objects.create(status="Active",posted_by=user, title=title, description=description,start_date=start_date, end_date=end_date, 
                               location=location)
        documents = self.context['request'].FILES.getlist('document', [])
        for document in documents:
            ProgramDocument.objects.create(status="Active", program=program, document=document)
        return validated_data
