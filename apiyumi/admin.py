from django.contrib import admin
from .models import *

admin.site.register([BusinessDetail, GraduatesDetail, Role, Resume])