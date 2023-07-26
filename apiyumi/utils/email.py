from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response


def signup_email(recipient, role):
    if role == 'host business':
        subject = 'signup success'
        message = 'Hi! You have successfully signed up as a host business for project YUMI. Thank You for being part of Project YUMI.'
    elif role == "graduate":
        subject = 'signup success'
        message = 'Hi! You have successfully signed up as a graduate for project YUMI. Thank You for being part of Project YUMI.'
    elif role == "volunteer":
        subject = 'signup success'
        message = 'Hi! You have successfully signed up as a volunteer for project YUMI. Thank You for being part of Project YUMI.'
    else:
        return Response(serializers.errors)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [f'{recipient}',]
    send_mail(subject, message, email_from, recipient_list)