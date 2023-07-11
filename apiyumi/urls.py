from django.urls import path
from .views import *

app_name = 'apiyumi'

urlpatterns = [
    #Login
    path('api/v1/auth/login/', UserLoginAPIView.as_view()),

    #Business end-points
    path('api/v1/auth/business/registrations/', BusinessregistrationAPIView.as_view()),
    path('api/v1/business/profile/', BusinessProfileAPIView.as_view()),


    #graduates end-points
    path('api/v1/auth/graduate/registrations/', GraduateRegistrationAPIView.as_view()),
    path('api/v1/graduate/profile/', GraduateProfileAPIView.as_view()),
]