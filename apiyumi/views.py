from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .utils import *
from rest_framework import status

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid()
        email = serializer.data['email']
        password = serializer.data['password']
        user = authenticate(username = email, password=password)
        try:
            if BusinessDetail.objects.filter(user=user):
                item = BusinessDetail.objects.filter(user=user).last()
                if item.status == "Active":
                    resp = {"tokens":get_tokens_for_user(user)}
                elif item.status == "Pending":
                    resp = {
                        "message" : "Account not active yet !"
                    }
                else:
                    resp = {
                        "message" : "Account disabled contact admin !"
                    }
            elif GraduatesDetail.objects.filter(user=user):
                item2 = GraduatesDetail.objects.filter(user=user).last()
                if item2.status == "Active":
                    # resp = {"tokens":get_tokens_for_user(user)}
                    resp = get_tokens_for_user(user)
                elif item2.status == "Pending":
                    resp = {
                        "message" : "Account not active yet !"
                    }
                else:
                    resp = {
                        "message" : "Account disabled contact admin !"
                    }
            else:
                resp = {
                        "message" : "invalid !"
                    }

        except Exception as e:
            print(e)
            resp = {
                "message": "Invalid credentials provided.."
            }
        return Response(resp)


#Business Classes API View
class BusinessregistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BusinessRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp = {
                'status': 'success',
                'data': serializer.data
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
        usr = request.user
        item = usr.businessdetail.id
        qset =  BusinessDetail.objects.get(id=item)
        serializer = BusinessProfileSerializer(qset)
        resp = {
            'status' : 'success',
            'data' : serializer.data
        }
        return Response(resp)
        

#Graduate classes APIView
class GraduateRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GraduateRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp = {
                'status': 'success',
                'data': serializer.data
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
        resp = {
            'status':status.HTTP_200_OK,
            'message' : 'success',
            'data' : serializer.data
        }
        return Response(resp)
    


#volunteer views

class volunteerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VolunteerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'success',
                'data' : serializer.data
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : serializer.errors
            }
        return Response(res)