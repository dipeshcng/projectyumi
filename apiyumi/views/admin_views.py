from rest_framework.views import APIView
from rest_framework.response import Response
from apiyumi.serializers.admin_serializers import *
from ..utils.permissions import SuperAdminOnlyPermission, AdminOnlyPermission
from rest_framework import status
from rest_framework.permissions import AllowAny
from apiyumi.models import Admin, BusinessDetail, GraduatesDetail, Volunteer, Job, Event
from datetime import date
from apiyumi.utils.validators import CustomPageNumberPagination


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
    pagination_class = CustomPageNumberPagination


    def get(self, request, pk=None):
        try:
            if pk is None:
                paginator = self.pagination_class()
                page_size = request.query_params.get('page_size', 10)
                paginator.page_size = int(page_size)
                qset = BusinessDetail.objects.all().order_by('-created_at')
                result_page = paginator.paginate_queryset(qset, request)
                serializer = BusinessProfileForAdminSerializer(result_page, many=True)
                data = {
                        'current_page': paginator.page.number,
                        'page_size': paginator.page_size,
                        'count': paginator.page.paginator.count,
                        'total_pages' : paginator.page.paginator.num_pages,
                        'next': paginator.get_next_link(),
                        'previous': paginator.get_previous_link(),
                        'results': serializer.data,
                        }
            else:
                qset = BusinessDetail.objects.get(id=pk)
                serializer = BusinessProfileForAdminSerializer(qset)
                data = serializer.data
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'success',
                'data' : data
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
    pagination_class = CustomPageNumberPagination


    def get(self, request, pk=None):
        try:
            if pk is None:
                paginator = self.pagination_class()
                page_size = request.query_params.get('page_size', 10)
                paginator.page_size = int(page_size)
                qset = GraduatesDetail.objects.all().order_by('-created_at')
                result_page = paginator.paginate_queryset(qset, request)
                serializer = GraduateDetailForAdminserializer(result_page, many=True, context={'request':request})
                data = {
                        'current_page': paginator.page.number,
                        'page_size': paginator.page_size,
                        'count': paginator.page.paginator.count,
                        'total_pages' : paginator.page.paginator.num_pages,
                        'next': paginator.get_next_link(),
                        'previous': paginator.get_previous_link(),
                        'results': serializer.data,
                        }
            else:
                qset = GraduatesDetail.objects.get(id=pk)
                serializer = GraduateDetailForAdminserializer(qset)
                data = serializer.data
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'success',
                'data' : data
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
    pagination_class = CustomPageNumberPagination


    def get(self, request, pk=None):
        try:
            if pk is None:
                paginator = self.pagination_class()
                page_size = request.query_params.get('page_size', 10)
                paginator.page_size = int(page_size)
                qset = Volunteer.objects.all().order_by('-created_at')
                result_page = paginator.paginate_queryset(qset, request)
                serializer = VolunteerDetailForAdminserializer(result_page, many=True)
                data = {
                        'current_page': paginator.page.number,
                        'page_size': paginator.page_size,
                        'count': paginator.page.paginator.count,
                        'total_pages' : paginator.page.paginator.num_pages,
                        'next': paginator.get_next_link(),
                        'previous': paginator.get_previous_link(),
                        'results': serializer.data,
                        }
            else:
                qset = Volunteer.objects.get(id=pk)
                serializer = VolunteerDetailForAdminserializer(qset)
                data = serializer.data
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'success',
                'data' : data
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


class TotalNumberObjectsAPIView(APIView):
    permission_classes = [SuperAdminOnlyPermission|AdminOnlyPermission]
    def get(self, request):
        try:
            jobs = Job.objects.all().count()
            business = BusinessDetail.objects.all().count()
            volunters = Volunteer.objects.all().count()
            graduates = GraduatesDetail.objects.all().count()
            events = Event.objects.all().count()
            res = {
                "status" : status.HTTP_200_OK,
                "total_jobs" : jobs,
                "total_events" : events,
                "total_business" : business,
                "total_volunteers" : volunters,
                "total_graduates" : graduates
            }
        except Exception as e:
            res = {
                "status" : status.HTTP_500_INTERNAL_SERVER_ERROR,
                "err_msg" : F'{e}'
            }
        return Response(res)
