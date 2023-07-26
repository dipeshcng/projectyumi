from django.urls import path, include
from .views import *
from . import views
from apiyumi.login import UserLoginAPIView
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('', views.BusinessregistrationAPIView)

app_name = 'apiyumi'


urlpatterns = [
    #Login
    path('api/v1/auth/login/', UserLoginAPIView.as_view()),

    #Business end-points
    path('api/v1/auth/business/registration/', BusinessregistrationAPIView.as_view()),
    path('api/v1/business/profile/', BusinessProfileAPIView.as_view()),


    #graduates end-points
    path('api/v1/auth/graduate/registration/', GraduateRegistrationAPIView.as_view()),
    path('api/v1/graduate/profile/', GraduateProfileAPIView.as_view()),

    
    #volunteer end-points
    path('api/v1/auth/volunteer/registration/', volunteerRegistrationView.as_view()),
    path('api/v1/volunteer/profile/', VolunteerProfileAPIView.as_view()),
]