from rest_framework.views import APIView
from apiyumi.serializers.reset_password_serializers import UserChangePasswordSerializer,UserSetNewPasswordSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.urls import reverse
from apiyumi.utils.email import Util
from rest_framework import status
from apiyumi.utils.permissions import loginRequiredPermission, BusinessOnlyPermission, VolunteerOnlyPermission, SuperAdminOnlyPermission
from django.urls import reverse_lazy

#reset password view
class UserResetPasswordRequestEmailAPIView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        email = request.data['email']
        if User.objects.filter(username=email).exists():
            usr = User.objects.get(username = email)
            uidb64 = urlsafe_base64_encode(smart_bytes(usr.id))
            token = PasswordResetTokenGenerator().make_token(usr)
            current_site = get_current_site(request=request).domain
            # relative_link = reverse('apiyumi:user-token-check', kwargs={'uidb64': uidb64, 'token': token})
            relative_link = reverse('apiyumi:user-token-check', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relative_link
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            data = {'email_body': email_body, 'to_email': usr.username,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            resp = {
                "status" : status.HTTP_200_OK,
                "message" : 'We have sent you a link to reset your password'
            }
            return Response(resp)

        #Fake response for fake user
        resp = {
                "status" : status.HTTP_200_OK,
                "message" : 'We have sent you a link to reset your password !'
            }
        return Response(resp)


class UserPasswordTokenCheckAPI(APIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                resp = {
                    "message" : "Token in not valid please request new one"
                }
                return Response(resp, status=status.HTTP_403_FORBIDDEN)
            resp = {
                "message" : "Token is Valid"
            }
            return Response(resp)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                resp = {
                    "message" : "Invalid Token"
                }
                return Response(resp, status=status.HTTP_403_FORBIDDEN)
            

class UserSetNewPasswordAPIView(APIView):
    def patch(self, request):
        serializer = UserSetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'status': "success", 'message': 'Password reset success'})
    

from django.views.generic import FormView
from django import forms
from django.contrib.auth import authenticate

class UserResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New Password'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New Password'
    }))

    def clean_confirm_password(self):
        newpwd = self.cleaned_data['new_password']
        cnfpwd = self.cleaned_data['confirm_password']

        if newpwd != cnfpwd:
            raise forms.ValidationError("Password did not match")
        return cnfpwd

from django.http import HttpResponse
from django.shortcuts import redirect



class UserPasswordResetPasswordView(FormView):
    template_name = "password_reset_confirm.html"
    form_class = UserResetPasswordForm
    # success_url = reverse_lazy("google.com")

    def form_valid(self, form):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        password = form.cleaned_data['confirm_password']
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            html= "Token invalid please request fro new token  " + '<a href="https://project-yumi-v2.vercel.app/auth/reset-password/">reset password</a>'
            return HttpResponse(html)
        else:
            user.set_password(password)
            user.save()
            return redirect('https://project-yumi-v2.vercel.app/')
    


#password change view
class UserPasswordChangeAPIView(APIView):
    permission_classes = [loginRequiredPermission,]

    def patch(self, request):
        self.user = request.user
        seriliazer = UserChangePasswordSerializer(data=request.data)
        try:
            if seriliazer.is_valid():
                if not self.user.check_password(seriliazer.data.get('old_password')):
                    res = {
                        'status' : status.HTTP_400_BAD_REQUEST,
                        'message' : 'wrong password'
                    }
                    return Response(res)
                self.user.set_password(seriliazer.data.get('new_password'))
                self.user.save()
                res = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'success'
                }
                return Response(res)
            else:
                res={
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : seriliazer.errors
                }
                return Response(res)
        except Exception as e:
            res = {
                'status' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message' : f'{e}'
            }
            return Response(res)