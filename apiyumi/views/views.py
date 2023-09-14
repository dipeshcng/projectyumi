from ..serializers.serializers import *
from ..models import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..utils.permissions import *
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from apiyumi.utils.email import SignUpEmailThread, ProfileUpdateEmailThread
from apiyumi.utils.utils import calculate_age, convert_date
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework import generics


#Business Classes API View
class BusinessregistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BusinessRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            serializer.save()
            role = 'host business'
            SignUpEmailThread(user_email, role).start()
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
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get(self, request):
        try:
            usr = request.user
            item = usr.hostbusiness.id
            qset =  BusinessDetail.objects.get(id=item)
            serializer = BusinessProfileSerializer(qset, context={'request': request})
            resp = {
                'status' : 'success',
                'data' : serializer.data
            }
            return Response(resp)
        except:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'messsage' : 'server error'})
    
    def patch(self, request, *args, **kwargs):
        usr = request.user
        item = usr.hostbusiness.id
        qset =  BusinessDetail.objects.get(id=item)
        serializer = BusinessProfileSerializer(qset,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            role = 'host business'
            ProfileUpdateEmailThread(usr.username, role).start()
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'update success'
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : serializer.errors
            }
        return Response(res)
        

#Graduate registration, profile, update view
class GraduateRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GraduateRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            serializer.save()
            role = 'graduate'
            SignUpEmailThread(user_email,role).start()           
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
        item = usr.graduate.id
        qset =  Resume.objects.get(user=item)
        serializer = ResumeSerializer(qset, context={'request':request})
        dob = serializer.data['user']['dob']
        age = calculate_age(dob)
        data = serializer.data
        data['age'] = age
        resp = {
            'status':status.HTTP_200_OK,
            'message' : 'success',
            'data' : data
        }
        return Response(resp)
    
    def patch(self, request):
        usr = request.user
        item = usr.graduate.id
        qset =  GraduatesDetail.objects.get(id=item)
        serializer = Graduateprofileserializer(qset,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            role = 'graduate'
            ProfileUpdateEmailThread(usr.username, role).start()
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'update success'
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : serializer.errors
            }
        return Response(res)
    


#volunteer registration, profile, update view
class volunteerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VolunteerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            serializer.save()
            role = 'volunteer'
            SignUpEmailThread(user_email, role).start()
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
    permission_classes = [VolunteerOnlyPermission]

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
    
    def patch(self, request):
        usr = request.user
        item = usr.volunteer.id
        qset =  Volunteer.objects.get(id=item)
        serializer = Volunteerprofileserializer(qset,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            role = 'volunteer'
            ProfileUpdateEmailThread(usr.username, role).start()
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'update success'
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : serializer.errors
            }
        return Response(res)


class VolunteerDeleteAPIView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, rquest, pk=None):
        user = Volunteer.objects.get(id=pk)
        user.delete()
        return Response({'message' : 'deleted'})
    
#Events Views
class EventCreateUpdateAPIView(APIView):
    permission_classes = [AdminOnlyPermission|SuperAdminOnlyPermission]

    def post(self, request):
        serializer = EventCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response('event created')
        else:
            return Response(serializer.errors)
    
    def patch(self, request, pk=None):
        try:
            event = Event.objects.get(id=pk)
            serializer = EventCreateSerializer(event,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'update success',
                }
            else:
                res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'error_message' : serializer.errors
                }
            
        except Exception as e:
            res = {'error_message': f'{e}'}
        
        return Response(res)

from datetime import date
from apiyumi.utils.validators import CustomPageNumberPagination
class EventListAPIView(APIView):
    permission_classes = [VolunteerOnlyPermission|GraduateOnlyPermission|SuperAdminOnlyPermission|AdminOnlyPermission]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        try:
            usr = request.user
            paginator = self.pagination_class()
            page_size = request.query_params.get('page_size', 10)
            paginator.page_size = int(page_size)
            if hasattr(usr, 'volunteer') | hasattr(usr, 'graduate'):
                event_list = Event.objects.all().order_by('-created_at').filter(status='Active', event_post_end_date__gte = str(date.today()))
            else:
                event_list = Event.objects.all().order_by('-created_at')
            result_page = paginator.paginate_queryset(event_list, request)
            serializer = EventListSerialzer(result_page, many=True)
            data = {
            'current_page': paginator.page.number,
            'page_size': paginator.page_size,
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data,
        }
            res = {
                'status' : status.HTTP_200_OK,
                'message': 'success',
                'data' : data
            }
        except Exception as e:
            res = {
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error_message' : f'{e}'
            }
        return Response(res)


class EventDetailAPIView(APIView):
    permission_classes = [VolunteerOnlyPermission|GraduateOnlyPermission|SuperAdminOnlyPermission|AdminOnlyPermission]

    def get(self, request, pk=None):
        try:
            user = request.user
            if hasattr(user, 'volunteer') or hasattr(user, 'graduate'):
                event = Event.objects.get(id=pk)
                if event.status == "Active" and event.event_post_end_date >= date.today():
                    serializer = EventDetailSerialzer(event)
                    if user in event.registered_by.all():
                        res = {
                            'status' : status.HTTP_200_OK,
                            'message' : 'success',
                            'data' : serializer.data,
                            'applied' : 'true'
                        }
                    else:
                        res = {
                            'status' : status.HTTP_200_OK,
                            'message' : 'success',
                            'data' : serializer.data,
                            'applied' : 'false'
                        }
                else:
                    res = {
                            'status' : status.HTTP_204_NO_CONTENT,
                            'error_message' : 'no events'
                        }
            else:
                event = Event.objects.get(id=pk)
                serializer = EventDetailForAdminSerialzer(event)
                res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'success',
                    'data' : serializer.data
                }

        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error_message' : f'{e}'
            }
        return Response(res)


class RegisterUnregisterForEventAPIView(APIView):
    permission_classes = [VolunteerOnlyPermission|GraduateOnlyPermission]

    def get(self, request, pk=None):
        user = request.user
        event = Event.objects.get(id=pk)
        if user not in event.registered_by.all():
            event.registered_by.add(user)
            event.save()
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'event apply success'
            }
        else:
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'already applied for this event'
            }
        return Response(res)
    

#job api views
class JobCreateUpdateAPIView(APIView):
    permission_classes = [AdminOnlyPermission|SuperAdminOnlyPermission|BusinessOnlyPermission]

    def post(self, request):
        serializer = JobCreateUpdateSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            res = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'job create success'
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error_message' : serializer.errors
            }
        return Response(res)
    
    def patch(self, request, pk=None):
        job = Job.objects.get(id=pk)
        serializer = JobCreateUpdateSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {
                'status' : status.HTTP_200_OK,
                'message' : 'job update success'
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error_message' : serializer.errors
            }
        return Response(res)

class JobListAPIView(APIView):
    permission_classes = [GraduateOnlyPermission|AdminOnlyPermission|SuperAdminOnlyPermission|BusinessOnlyPermission]

    def get(self, request):
        user = request.user
        if hasattr(user, 'graduate'):
            job_qs = Job.objects.filter(status="Active", application_end_date__gte = str(date.today())).order_by("-created_at")
            serializer = JobListDetailSerializer(job_qs,many=True, context={'request':request})
        elif hasattr(user, 'hostbusiness'):
            job_qs = Job.objects.filter(posted_by=user).order_by("-created_at")
            serializer = JobListDetailForAdminSerializer(job_qs,many=True, context={'request':request})
            data = serializer.data
        else:
            job_qs = Job.objects.all().order_by("-created_at")
            serializer = JobListDetailForAdminSerializer(job_qs, many=True, context = {'request': request})
            
        res = {
            "status" : status.HTTP_200_OK,
            "data" : serializer.data
        }
        return Response(res)
        
    

class JobDetailAPIView(APIView):
    permission_classes = [GraduateOnlyPermission|BusinessOnlyPermission|SuperAdminOnlyPermission|AdminOnlyPermission]

    def get(self, request,pk=None):
        try:
            user = request.user
            if hasattr(user, 'graduate'):
                job = Job.objects.filter(id=pk,status='Active', application_end_date__gte = str(date.today())).first()
                serializer = JobListDetailSerializer(job, context={'request' : request})
                res = {
                    'status' : status.HTTP_200_OK,
                    'data' : serializer.data
                }
            elif hasattr(user, 'hostbusiness'):
                job = Job.objects.filter(id=pk,posted_by=user).first()
                serializer = JobListDetailForAdminSerializer(job, context = {'request':request})
                res = {
                    'status' : status.HTTP_200_OK,
                    'data' : serializer.data
                }
            else:
                job = Job.objects.get(id=pk)
                serializer = JobListDetailForAdminSerializer(job, context={'request' : request})
                res = {
                    'status' : status.HTTP_200_OK,
                    'data' : serializer.data
                }
            return Response(res)
        except Exception as e:
            return Response(f'{e}')
    

class JobRegisterAPIView(APIView):
    permission_classes = [GraduateOnlyPermission]

    def get(self, request, pk=None):
        user = request.user
        job = Job.objects.get(id=pk)
        if user not in job.applied_by.all():
            resume_id = self.request.GET.get('resume_id', None)
            grad = GraduatesDetail.objects.get(user=user)
            resume = Resume.objects.filter(id=resume_id, user=grad).last()
            if resume:
                job.applied_by.add(user)
                job.resume.add(resume)
                job.save()
                res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'job apply success'
                }
            else:
                res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'upload resume first'
                }
        else:
            res = {
                'status' : status.HTTP_308_PERMANENT_REDIRECT,
                'message' : 'already applied for this job'
            }
        return Response(res)