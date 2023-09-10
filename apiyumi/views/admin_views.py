from rest_framework.views import APIView
from rest_framework.response import Response
from apiyumi.serializers.admin_serializers import *
from ..utils.permissions import SuperAdminOnlyPermission, AdminOnlyPermission
from rest_framework import status
from rest_framework.permissions import AllowAny
from apiyumi.models import Admin, BusinessDetail, GraduatesDetail, Volunteer


class AdminRegistrationAPIView(APIView):
    permission_classes = [SuperAdminOnlyPermission, ]

    def post(self, request):
        print(request.data)
        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'created'
            }
        else:
            resp = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : serializer.errors
            }
        return Response (resp)


class AdminProfileView(APIView):
    permission_classes = [AdminOnlyPermission, ]

    def get(self, request):
        try:
            user = request.user
            admin = Admin.objects.filter(user=user).first()
            serializer = AdminProfileserialzer(admin)
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'success',
                'data' : {
                    'email' : serializer.data['user']['username'],
                    'full_name' : serializer.data['full_name']
                }
            }
            return Response(res)
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
            return Response(res)

#List API
class BusinessListForAdminAPIView(APIView):
    permission_classes = [SuperAdminOnlyPermission|AdminOnlyPermission]

    def get(self, request, pk=None):
        try:
            if pk is None:
                qset = BusinessDetail.objects.all().order_by('-created_at')
                serializer = BusinessProfileForAdminSerializer(qset, many=True)
            else:
                qset = BusinessDetail.objects.get(id=pk)
                serializer = BusinessProfileForAdminSerializer(qset)
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'success',
                'data' : serializer.data
            }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)

    def patch(self, request, pk=None):
        try:
            item = BusinessDetail.objects.get(id=pk)
            serializer = BusinessProfileForAdminSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {
                'status' : status.HTTP_200_OK,
                'message' : 'update success'
            }
            else:
                res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'error' : serializer.errors
                }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)


class GraduateListForAdminAPIView(APIView):
    permission_classes = [SuperAdminOnlyPermission|AdminOnlyPermission]

    def get(self, request, pk=None):
        try:
            if pk is None:
                qset = GraduatesDetail.objects.all().order_by('-created_at')
                serializer = GraduateDetailForAdminserializer(qset, many=True)
            else:
                qset = GraduatesDetail.objects.get(id=pk)
                serializer = GraduateDetailForAdminserializer(qset)
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'success',
                'data' : serializer.data
            }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)
    
    def patch(self, request, pk=None):
        try:
            item = GraduatesDetail.objects.get(id=pk)
            serializer = GraduateDetailForAdminserializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {
                'status' : status.HTTP_200_OK,
                'message' : 'update success'
            }
            else:
                res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'error' : serializer.errors
                }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)


class VolunteerListForAdminAPIView(APIView):
    permission_classes = [SuperAdminOnlyPermission|AdminOnlyPermission]

    def get(self, reques, pk=None):
        try:
            if pk is None:
                qset = Volunteer.objects.all().order_by('-created_at')
                serializer = VolunteerDetailForAdminserializer(qset, many=True)
            else:
                qset = Volunteer.objects.get(id=pk)
                serializer = VolunteerDetailForAdminserializer(qset)
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'success',
                'data' : serializer.data
            }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)
    
    def patch(self, request, pk=None):
        try:
            item = Volunteer.objects.get(id=pk)
            serializer = VolunteerDetailForAdminserializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {
                'status' : status.HTTP_200_OK,
                'message' : 'update success'
            }
            else:
                res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'error' : serializer.errors
                }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)