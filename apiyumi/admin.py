from django.contrib import admin
from .models import *

admin.site.register([Admin,BusinessDetail, GraduatesDetail, Role, Resume, Volunteer, Event, Job, JobMessage])