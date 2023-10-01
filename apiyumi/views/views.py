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
import json



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

    # def get(self, request):
    #     usr = request.user
    #     item = usr.graduate.id
    #     qset =  Resume.objects.get(user=item)
    #     serializer = ResumeSerializer(qset, context={'request':request})
    #     dob = serializer.data['user']['dob']
    #     age = calculate_age(dob)
    #     data = serializer.data
    #     data['age'] = age
    #     resp = {
    #         'status':status.HTTP_200_OK,
    #         'message' : 'success',
    #         'data' : data
    #     }
    #     return Response(resp)

    def get(self, request):
        usr = request.user
        # resume_qs = Resume.objects.filter(user = usr)
        grad = GraduatesDetail.objects.get(user=usr)
        serializer = GraduatesDetailSerializer(grad, context={'request':request})
        resp = {
            'status':status.HTTP_200_OK,
            'message' : 'success',
            'data' : serializer.data
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
            res = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Event create success'
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error_message' : serializer.errors
            }
        return Response(res)
    
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
    
    def delete(self, request, pk=None):
        try:
            event = Event.objects.get(id=pk)
            event.delete()
            res = {
                        'status' : status.HTTP_200_OK,
                        'message' : 'delete success'
                    }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)

from datetime import date
from apiyumi.utils.validators import CustomPageNumberPagination
class EventListAPIView(APIView):
    permission_classes = [VolunteerOnlyPermission|GraduateOnlyPermission|SuperAdminOnlyPermission|AdminOnlyPermission|BusinessOnlyPermission]
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
            'total_pages' : paginator.page.paginator.num_pages,
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
    permission_classes = [VolunteerOnlyPermission|GraduateOnlyPermission|SuperAdminOnlyPermission|AdminOnlyPermission|BusinessOnlyPermission]

    def get(self, request, pk=None):
        try:
            user = request.user
            if hasattr(user, 'volunteer') or hasattr(user, 'graduate') or hasattr(user, 'hostbusiness'):
                event = Event.objects.get(id=pk)
                if event.status == "Active" and event.event_post_end_date >= date.today():
                    serializer = EventDetailSerialzer(event, context={'request':request})
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
                serializer = EventDetailForAdminSerialzer(event, context={'request':request})
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
    permission_classes = [VolunteerOnlyPermission|GraduateOnlyPermission|BusinessOnlyPermission]

    def post(self, request, pk=None):
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
    
    def delete(self, request, pk=None):
        try:
            job = Job.objects.get(id=pk)
            user = request.user
            if user.is_superuser == True or hasattr(user, 'admin'):
                job.delete()
                res = {
                        'status' : status.HTTP_200_OK,
                        'message' : 'delete success'
                    }
            elif hasattr(user, 'hostbusiness') and job.posted_by == user:
                job.delete()
                res = {
                        'status' : status.HTTP_200_OK,
                        'message' : 'delete success'
                    }
            else:
                res = {
                    'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'permission denied'
                }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)



class JobListAPIView(APIView):
    permission_classes = [GraduateOnlyPermission|AdminOnlyPermission|SuperAdminOnlyPermission|BusinessOnlyPermission]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        try:
            user = request.user
            paginator = self.pagination_class()
            page_size = request.query_params.get('page_size', 10)
            paginator.page_size = int(page_size)
            if hasattr(user, 'graduate'):
                job_qs = Job.objects.filter(status="Active", application_end_date__gte = str(date.today())).order_by("-created_at")
                result_page = paginator.paginate_queryset(job_qs, request)
                serializer = JobListDetailSerializer(result_page,many=True, context={'request':request})
            elif hasattr(user, 'hostbusiness'):
                job_qs = Job.objects.filter(posted_by=user).order_by("-created_at")
                result_page = paginator.paginate_queryset(job_qs, request)
                serializer = JobListForAdminSerializer(result_page,many=True, context={'request':request})
            elif hasattr(user, 'admin'):
                job_qs = Job.objects.all().order_by("-created_at")
                result_page = paginator.paginate_queryset(job_qs, request)
                serializer = JobListForAdminSerializer(result_page, many=True, context = {'request': request})
            data = {
                'current_page': paginator.page.number,
                'page_size': paginator.page_size,
                'count': paginator.page.paginator.count,
                'total_pages' : paginator.page.paginator.num_pages,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': serializer.data,
            }
            res = {
                "status" : status.HTTP_200_OK,
                "data" : data
            }
        except Exception as e:
            res = {
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error_message' : f'{e}'
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
                serializer = JobListDetailForAdminSerializer(job, context = {'request':request, 'job':job})
                res = {
                    'status' : status.HTTP_200_OK,
                    'data' : serializer.data
                }
            else:
                job = Job.objects.get(id=pk)
                serializer = JobListDetailForAdminSerializer(job, context={'request' : request, 'job':job})
                res = {
                    'status' : status.HTTP_200_OK,
                    'data' : serializer.data
                }
            return Response(res)
        except Exception as e:
            return Response(f'{e}')
    
class JobRegisterAPIView(APIView):
    permission_classes = [GraduateOnlyPermission]
    parser_classes = [FormParser, MultiPartParser, JSONParser]


    def post(self, request, pk=None):
        try:
            user = request.user
            job = Job.objects.get(id=pk)
            if user not in job.applied_by.all():
                data = json.loads(request.body.decode('utf-8'))
                resume_id = data.get('resume_id')
                message = data.get('message')
                graduate = GraduatesDetail.objects.get(user=user)
                resume = Resume.objects.filter(id=resume_id, user=user.graduate).last()
                if resume and message:
                    job.applied_by.add(user)
                    job.resume.add(resume)
                    job.save()
                    JobMessage.objects.create(status="Active",user=user, job=job,message=message)
                    res = {
                        'status' : status.HTTP_200_OK,
                        'message' : 'job apply success'
                    }
                else:
                    res = {
                        'status' : status.HTTP_200_OK,
                        'message' : 'upload resume first and also message cannot be empty'
                    }
            else:
                res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'err_message' : 'already applied for this job'
                }
        except Exception as e:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_message' : f'{e}'
            }
        return Response(res)


#Resume
class ResumeCreateAPIView(APIView):
    permission_classes = [GraduateOnlyPermission]

    def post(self, request):
        serializer = ResumeCreateSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'resume upload success'
                }
        else:
            res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'err_message' : serializer.errors
                }
        return Response(res)
    
    def delete(self, request, pk=None):
        try:
            graduate = request.user.graduate
            resume = Resume.objects.get(id=pk)
            if resume.user == graduate:
                resume.delete()
                res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'resume delete success'
                }
            else:
                res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_message' : 'permission denied'
            }
        except Exception as e:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_message' : f'{e}'
            }
        return Response(res)


#Programs
class ProgramCreateUpdateAPIView(APIView):
    permission_classes = [AdminOnlyPermission|SuperAdminOnlyPermission]
    # parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ProgramSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            res = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'program create success'
            }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_message' : serializer.errors
            }
        return Response(res)

    def patch(self, request, pk=None):
        try:
            program = Program.objects.get(id=pk)
            serializer = ProgramSerializer(program, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {
                    'status' : status.HTTP_201_CREATED,
                    'message' : 'program update success'
                }
            else:
                res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'err_message' : serializer.errors
                }
        except Exception as e:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_message' : f'{e}'
            }
        return Response(res)
    
    def delete(self, request,pk=None):
        try:
            program = Program.objects.get(id=pk)
            program.delete()
            res = {
                        'status' : status.HTTP_200_OK,
                        'message' : 'delete success'
                    }
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
        return Response(res)


class ProgramListDetailAPIView(APIView):
    permission_classes = [GraduateOnlyPermission|VolunteerOnlyPermission|AdminOnlyPermission|SuperAdminOnlyPermission]
    pagination_class = CustomPageNumberPagination
    def get(self, request, pk=None):
        try:
            if pk is None:
                programs = Program.objects.filter(status="Active")
                paginator = self.pagination_class()
                page_size = request.query_params.get('page_size', 10)
                paginator.page_size = int(page_size)
                result_page = paginator.paginate_queryset(programs, request)
                serializer = ProgramListSerializer(result_page, many=True)
                data = {
                'current_page': paginator.page.number,
                'page_size': paginator.page_size,
                'count': paginator.page.paginator.count,
                'total_pages' : paginator.page.paginator.num_pages,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': serializer.data,
            }
                res = {
                    'status' : status.HTTP_200_OK,
                    'data' : data
                    }
            else:
                user = request.user
                program = Program.objects.get(id=pk)
                registered_by_count = program.registered_by.count()
                if hasattr(user, 'volunteer'):
                    serializer = ProgramListSerializer(program, context={'request':request})
                    data = serializer.data
                    res = {
                    'status' : status.HTTP_200_OK,
                    'data' : data
                    }
                elif hasattr(user, 'graduate') or hasattr(user, 'volunteer'):
                    serializer = ProgramDetailSerializer(program, context={'request':request})
                    data = serializer.data
                    data['register'] = registered_by_count
                    res = {
                    'status' : status.HTTP_200_OK,
                    'data' : data
                    }
                else:
                    serializer = ProgramDetailSerializer(program, context={'request':request})
                    data = serializer.data
                    data['register'] = registered_by_count
                    res = {
                        'status' : status.HTTP_200_OK,
                        'data' : data
                        }
        except Exception as e:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_message' : f'{e}'
            }
        return Response(res)

class ProgramRegisterAPIView(APIView):
    permission_classes = [GraduateOnlyPermission|VolunteerOnlyPermission|BusinessOnlyPermission]

    def post(self, request, pk=None):
        try:
            user = request.user
            program = Program.objects.get(id=pk)
            if user not in program.registered_by.all():
                    program.registered_by.add(user)
                    program.save()
                    res = {
                        'status' : status.HTTP_200_OK,
                        'message' : 'program apply success'
                    }
            else:
                res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'err_message' : 'already applied for this job'
                }
        except Exception as e:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_message' : f'{e}'
            }
        return Response(res)

class ProgramDocumentCreateDeleteAPIView(APIView):
    permission_classes = [AdminOnlyPermission|SuperAdminOnlyPermission]

    def post(self, request, program_id=None):
        program = Program.objects.get(id=program_id)
        serializer = ProgramDocumentSerializer(data=request.FILES, context={'program':program, 'request':request})
        if serializer.is_valid():
            serializer.save()
            res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'document create success'
                    }
        else:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_messsage' : serializer.errors
            }
        return Response(res)


    def delete(self, request, program_id=None, document_id=None):
        try:
            program = Program.objects.get(id=program_id)
            document = ProgramDocument.objects.get(id=document_id)
            if document in program.programdocument_set.all():
                document.delete()
                res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'document delete success'
                    }
            else:
                res = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Document Doestnot exists !!'
                    }
        except Exception as e:
            res = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'err_message' : f'{e}'
            }
        return Response(res)

