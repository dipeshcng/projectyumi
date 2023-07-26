from django.db import models
from django.contrib.auth.models import User
from .constants import *


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
    

# class Admin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)

#     full_name = models.CharField(max_length=100)



class BusinessDetail(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)

    #for business
    name_of_business = models.CharField(max_length=100)
    business_logo = models.ImageField(upload_to='business/logo', null=True, blank=True)
    business_contact = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    number_of_employee = models.IntegerField(null=True, blank=True)
    level_of_recruitment = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


    def __str__(self) -> str:
        return self.name_of_business


class GraduatesDetail(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

     #For Graduates
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    image = models.ImageField(upload_to='user/graduate', null=True, blank=True)
    phone = models.CharField(max_length=15)
    # cv = models.FileField(upload_to='files', null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name


class Volunteer(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user/volunteer', null=True, blank=True)

    def __str__(self):
        return f'{self.user}'


class Resume(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='resume')

    def __str__(self):
        return f'{self.user} resume for {self.title}'