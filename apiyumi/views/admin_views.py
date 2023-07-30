from rest_framework.views import APIView
from rest_framework.response import Response
from apiyumi.serializers.admin_serializers import AdminRegistrationSerializer, AdminProfileserialzer
from ..utils.permissions import SuperAdminOnlyPermission, AdminOnlyPermission
from rest_framework import status
from rest_framework.permissions import AllowAny
from apiyumi.models import Admin


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