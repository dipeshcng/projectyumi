from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from django.core.mail import EmailMessage
import threading



# def signup_email(recipient, role):
#     if role == 'host business':
#         subject = 'signup success'
#         message = 'Hi! You have successfully signed up as a host business for project YUMI. Thank You for being part of Project YUMI.'
#     elif role == "graduate":
#         subject = 'signup success'
#         message = 'Hi! You have successfully signed up as a graduate for project YUMI. Thank You for being part of Project YUMI.'
#     elif role == "volunteer":
#         subject = 'signup success'
#         message = 'Hi! You have successfully signed up as a volunteer for project YUMI. Thank You for being part of Project YUMI.'
#     else:
#         return Response(serializers.errors)
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [f'{recipient}',]
#     send_mail(subject, message, email_from, recipient_list)


# def Profile_Update_email(recipient, role):
#     if role == 'host business':
#         subject = 'signup success'
#         message = 'Hi! profile update successfull. Thank You for being part of Project YUMI.'
#     elif role == "graduate":
#         subject = 'signup success'
#         message = 'Hi! profile update successfull. Thank You for being part of Project YUMI.'
#     elif role == "volunteer":
#         subject = 'signup success'
#         message = 'Hi! profile update successfull. Thank You for being part of Project YUMI.'
#     else:
#         return Response(serializers.errors)
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [f'{recipient}',]
#     send_mail(subject, message, email_from, recipient_list)

class SignUpEmailThread(threading.Thread):
    
    def __init__(self, recipient, role, ):
        if role == 'host business':
            self.subject = 'signup success'
            self.message = 'Hi! You have successfully signed up as a host business for project YUMI. Thank You for being part of Project YUMI.'
        elif role == "graduate":
            self.subject = 'signup success'
            self.message = 'Hi! You have successfully signed up as a graduate for project YUMI. Thank You for being part of Project YUMI.'
        elif role == "volunteer":
            self.subject = 'signup success'
            self.message = 'Hi! You have successfully signed up as a volunteer for project YUMI. Thank You for being part of Project YUMI.'
        else:
            return Response(serializers.errors)
        self.email_from = settings.EMAIL_HOST_USER
        self.recipient_list = [f'{recipient}',]
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.message, self.email_from, self.recipient_list)


class ProfileUpdateEmailThread(threading.Thread):
    
    def __init__(self, recipient, role, ):
        if role == 'host business':
            self.subject = 'signup success'
            self.message = 'Hi! profile update successfull. Thank You for being part of Project YUMI.'
        elif role == "graduate":
            self.subject = 'signup success'
            self.message = 'Hi! profile update successfull. Thank You for being part of Project YUMI.'
        elif role == "volunteer":
            self.subject = 'signup success'
            self.message = 'Hi! profile update successfull. Thank You for being part of Project YUMI.'
        else:
            return Response(serializers.errors)
        self.email_from = settings.EMAIL_HOST_USER
        self.recipient_list = [f'{recipient}',]
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.message, self.email_from, self.recipient_list)

class EmailThread(threading.Thread):
    
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
        
class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()