from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate
from .models import BusinessDetail, GraduatesDetail, Volunteer
from apiyumi.utils.permissions import get_tokens_for_user




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