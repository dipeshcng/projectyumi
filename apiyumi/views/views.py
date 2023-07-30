from ..serializers.serializers import *
from ..models import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..utils.permissions import *
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from apiyumi.utils.email import signup_email
from apiyumi.utils.utils import calculate_age


#Business Classes API View
class BusinessregistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BusinessRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            serializer.save()
            role = 'host business'
            signup_email(user_email, role)
            resp = {
                'status':status.HTTP_201_CREATED,
                'message' : 'created',
            }
            return Response(resp)
        else:
            resp = {
                "message":serializer.errors
            }
            return Response(resp)
        

class BusinessProfileAPIView(APIView):
    permission_classes = [BusinessOnlyPermission]

    def get(self, request):
        try:
            usr = request.user
            item = usr.businessdetail.id
            qset =  BusinessDetail.objects.get(id=item)
            serializer = BusinessProfileSerializer(qset)
            resp = {
                'status' : 'success',
                'data' : serializer.data
            }
            return Response(resp)
        except:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'messsage' : 'server error'})
        

#Graduate classes APIView
class GraduateRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GraduateRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            serializer.save()
            role = 'graduate'
            signup_email(user_email,role)
            resp = {
                'status': status.HTTP_201_CREATED,
                'data': 'created'
            }
            return Response(resp)
        else:
            resp = {
                "message":serializer.errors
            }
            return Response(resp)

class GraduateProfileAPIView(APIView):
    permission_classes = [GraduateOnlyPermission]

    def get(self, request):
        usr = request.user
        item = usr.graduatesdetail.id
        qset =  GraduatesDetail.objects.get(id=item)
        serializer = Graduateprofileserializer(qset, context={'request':request})
        dob = qset.dob
        age = calculate_age(dob)
        data = serializer.data
        data['age'] = age
        resp = {
            'status':status.HTTP_200_OK,
            'message' : 'success',
            'data' : data
        }
        return Response(resp)
    


#volunteer views

class volunteerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VolunteerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            serializer.save()
            role = 'volunteer'
            signup_email(user_email, role)
            res = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'created',
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : serializer.errors
            }
        return Response(res)
    

class VolunteerProfileAPIView(APIView):
    permission_classes = [VolunteerOnlyPermission, ]

    def get(self, request):
        usr = request.user
        item = usr.volunteer.id
        qset =  Volunteer.objects.get(id=item)
        serializer = Volunteerprofileserializer(qset, context={'request':request})
        resp = {
            'status':status.HTTP_200_OK,
            'message' : 'success',
            'data' : serializer.data
        }
        return Response(resp)