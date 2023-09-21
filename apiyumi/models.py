from django.db import models
from django.contrib.auth.models import User
from .utils.constants import *
from django.conf import settings

from enum import IntEnum



class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')

    class Meta:
        abstract=True


class Role(TimeStamp):
    role_type = models.CharField(max_length=100)

    def __str__(self):
        return self.role_type
    

class Admin(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='admin')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name



class BusinessDetail(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='hostbusiness')
    role = models.ForeignKey(Role,on_delete=models.CASCADE)

    #for business
    name_of_business = models.CharField(max_length=100)
    business_logo = models.ImageField(null=True, blank=True)
    business_contact = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    number_of_employee = models.IntegerField(null=True, blank=True)
    level_of_recruitment = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


    def __str__(self) -> str:
        return self.name_of_business

# class WorkingStatus(IntEnum):
#   LookingForJob = 1
#   Internship = 2
#   Working = 3
  
#   @classmethod
#   def choices(cls):
#     return [(key.value, key.name) for key in cls]
  
class GraduatesDetail(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='graduate')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    working_status = models.CharField(max_length=100,choices=WORKING_STATUS, default="Looking for job", null=True, blank=True)
     #For Graduates
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    image = models.ImageField(upload_to='user/graduate', null=True, blank=True)
    phone = models.CharField(max_length=15)
    # cv = models.FileField(upload_to='files', null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name


class Volunteer(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='volunteer')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user/volunteer', null=True, blank=True)

    def __str__(self):
        return f'{self.user}'
    
    @property
    def image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)


class Resume(TimeStamp):
    user = models.ForeignKey(GraduatesDetail, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='resume')

    def __str__(self):
        return f'{self.user} resume'


class Job(TimeStamp):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    salary_type = models.CharField(max_length=30, choices=SALARY_STATUS)
    salary = models.PositiveBigIntegerField(default=0)
    no_of_hires = models.PositiveIntegerField()
    requirements = models.TextField()
    application_start_date = models.DateField()
    application_end_date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.FileField(null=True, blank=True)

    applied_by = models.ManyToManyField(User, related_name='job_applied_by', blank=True)
    resume = models.ManyToManyField(Resume, blank=True, related_name="job_resume")

    def __str__(self):
        return self.title


class Event(TimeStamp):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_created_by')

    event_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    document = models.FileField(null=True, blank=True)
    event_start_date = models.DateTimeField(null=True, blank=True)
    event_end_date = models.DateTimeField(null=True, blank=True)

    event_post_end_date = models.DateField(null=True, blank=True)

    registered_by = models.ManyToManyField(User, related_name="event_registed_by", blank=True)

    def __str__(self):
        return self.event_name

class JobMessage(TimeStamp):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)

    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.job.id)
    
class Program(TimeStamp):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program')
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    document = models.FileField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_slots = models.PositiveIntegerField(null=True, blank=True)
    registered_by = models.ManyToManyField(User, related_name="program_registered_by", blank=True)

    def __str__(self):
        return self.title
