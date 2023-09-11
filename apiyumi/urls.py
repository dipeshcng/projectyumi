from django.urls import path, include
from .views.views import *
from .views.reset_password import UserResetPasswordRequestEmailAPIView, UserPasswordTokenCheckAPI, UserSetNewPasswordAPIView, \
    UserPasswordChangeAPIView

from apiyumi.views.login import UserLoginAPIView, DecodeTokenView, DecodeTokenForSingleUserView
from rest_framework import routers
from apiyumi.views.admin_views import *

# router = routers.DefaultRouter()
# router.register('', views.BusinessregistrationAPIView)

app_name = 'apiyumi'

urlpatterns = [
    #Login
    path('api/v1/auth/login/', UserLoginAPIView.as_view()),
    # path('api/v1/auth/accounts/', DecodeTokenView.as_view()),
    path('api/v1/auth/account/', DecodeTokenForSingleUserView.as_view()),

    #reset password
    path('api/v1/user/request-reset-email/', UserResetPasswordRequestEmailAPIView.as_view()),
    path('api/v1/user/password-reset/check/token/<uidb64>/<token>/',UserPasswordTokenCheckAPI.as_view(), name="user-token-check"),
    path('api/v1/user/password-reset-complete/', UserSetNewPasswordAPIView.as_view(),),

    #change password
    path('api/v1/user/password-change/', UserPasswordChangeAPIView.as_view()),
    
    #admin
    path('api/v1/auth/admin/registration/', AdminRegistrationAPIView.as_view()),
    path('api/v1/admin/profile/', AdminProfileView.as_view()),


    #Business end-points
    path('api/v1/auth/business/registration/', BusinessregistrationAPIView.as_view()),
    path('api/v1/business/profile/', BusinessProfileAPIView.as_view()), 
    # """get and patch request with same url"""


    #graduates end-points
    path('api/v1/auth/graduate/registration/', GraduateRegistrationAPIView.as_view()),
    path('api/v1/graduate/profile/', GraduateProfileAPIView.as_view()),
    #get and patch request with same url

    
    #volunteer end-points
    path('api/v1/auth/volunteer/registration/', volunteerRegistrationView.as_view()),
    path('api/v1/volunteer/profile/', VolunteerProfileAPIView.as_view()),
    #get and patch request with same url

    # path('api/v1/volunteer/<int:pk>/', VolunteerDeleteAPIView.as_view()),


    #event end-points
    path('api/v1/event/', EventCreateUpdateAPIView.as_view()),
    path('api/v1/event/<int:pk>/', EventCreateUpdateAPIView.as_view()),
    path('api/v1/event/list/', EventListAPIView.as_view()),
    path('api/v1/event/detail/<int:pk>/', EventDetailAPIView.as_view()),
    path('api/v1/event/register-unregister/<int:pk>/', RegisterUnregisterForEventAPIView.as_view()),

    
    #job end-points
    path('api/v1/job/', JobCreateUpdateAPIView.as_view()),
    path('api/v1/job/<int:pk>/', JobCreateUpdateAPIView.as_view()),
    path('api/v1/job-list/', JobListAPIView.as_view()),
    path('api/v1/job/<int:pk>/details/', JobDetailAPIView.as_view()),
    path('api/v1/job/<int:pk>/register/', JobRegisterAPIView.as_view()),

    #end-points for admin for list of businessdetail, volunteer and graduate
    path('api/v1/business/', BusinessListForAdminAPIView.as_view()),
    path('api/v1/volunteer/', VolunteerListForAdminAPIView.as_view()),
    path('api/v1/graduate/', GraduateListForAdminAPIView.as_view()),

    #end-points for admin for detail and update of businessdetail, volunteer and graduate
    path('api/v1/business/<int:pk>/', BusinessListForAdminAPIView.as_view()),
    path('api/v1/volunteer/<int:pk>/', VolunteerListForAdminAPIView.as_view()),
    path('api/v1/graduate/<int:pk>/', GraduateListForAdminAPIView.as_view()),

]