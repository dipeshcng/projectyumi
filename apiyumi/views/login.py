from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.serializers import UserLoginSerializer
from django.contrib.auth import authenticate
from ..models import BusinessDetail, GraduatesDetail, Volunteer, Admin
from apiyumi.utils.permissions import get_tokens_for_user
from django.contrib.auth.models import User




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
                    resp = get_tokens_for_user(user)
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
            elif Volunteer.objects.filter(user=user):
                item2 = Volunteer.objects.filter(user=user).last()
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
            elif Admin.objects.filter(user=user):
                item3 = Admin.objects.filter(user=user).last()
                if item3.status == "Active":
                    # resp = {"tokens":get_tokens_for_user(user)}
                    resp = get_tokens_for_user(user)
                elif item3.status == "Pending":
                    resp = {
                        "message" : "Account not active yet !"
                    }
                else:
                    resp = {
                        "message" : "Account disabled contact admin !"
                    }
            elif user.is_superuser:
                resp = get_tokens_for_user(user)
            else:
                resp = {
                        "message" : "invalid !"
                    }

        except Exception as e:
            print(e)
            resp = {
                "message": "Invalid credentials provided.."
            }
        return Response({'access_token' : resp})
    

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import TokenError
from django.contrib.auth.models import User

class DecodeTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            users = User.objects.all()

            # Create a list of serialized user data
            serialized_users = []
            for user in users:
                if hasattr(user, 'admin'):
                    role = ['ADMIN']
                elif hasattr(user, 'volunteer'):
                    role = [' VOLUNTEER']
                elif hasattr(user, 'graduate'):
                    role = ['GRADUATE']
                elif hasattr(user, 'hostbusiness'):
                    role = ['BUSINESS']
                else:
                    role = ['SUPERADMIN']

                serialized_data = {
                    'email': user.username,
                    'roles' : role
                    
                }
                serialized_users.append(serialized_data)

            return Response(serialized_users)

        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class DecodeTokenForSingleUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # serialized_user = []
            user = request.user
            if hasattr(user, 'admin'):
                role = ['ADMIN']
            elif hasattr(user, 'volunteer'):
                role = ['VOLUNTEER']
            elif hasattr(user, 'graduate'):
                role = ['GRADUATE']
            elif hasattr(user, 'hostbusiness'):
                role = ['BUSINESS']
            else:
                role = ['SUPERADMIN']

            serialized_data = {
                'email': user.username,
                'roles' : role
                
            }
            # serialized_user.append(serialized_data)
            return Response(serialized_data)

        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
