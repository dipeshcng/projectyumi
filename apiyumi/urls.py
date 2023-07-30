from django.urls import path, include
from .views.views import *
from .views.reset_password import UserResetPasswordRequestEmailAPIView, UserPasswordTokenCheckAPI, UserSetNewPasswordAPIView, \
    UserPasswordChangeAPIView

from apiyumi.views.login import UserLoginAPIView
from rest_framework import routers
from apiyumi.views.admin_views import AdminRegistrationAPIView, AdminProfileView

# router = routers.DefaultRouter()
# router.register('', views.BusinessregistrationAPIView)

app_name = 'apiyumi'

urlpatterns = [
    #Login
    path('api/v1/auth/login/', UserLoginAPIView.as_view()),

    #reset password
    path('api/v1/user/request-reset-email/', UserResetPasswordRequestEmailAPIView.as_view()),
    path('api/v1/user/password-reset/check/token/<uidb64>/<token>/',UserPasswordTokenCheckAPI.as_view(), name="user-token-check"),
    path('api/v1/user/password-reset-complete/', UserSetNewPasswordAPIView.as_view(),),

    #change password
    path('api/v1/user/password-change/', UserPasswordChangeAPIView.as_view()),
    
    #admin
    path('api/v1/auth/admin/registration', AdminRegistrationAPIView.as_view()),
    path('api/v1/admin/profile/', AdminProfileView.as_view()),


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