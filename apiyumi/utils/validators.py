from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

def validate_email(email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "email already exists"})
        return email
    

def validate_password(value):
    if value.isalnum():
        raise serializers.ValidationError({'error' : 'password must have atleast one special character.'})
    # if len(value) < 6:
    #     raise serializers.ValidationError({'error' : 'password minimum length is 6 character.'})
    return value


def validate_graduate_age(value):
    if value < 16:
        raise serializers.ValidationError({'error':'graduate must be above 16 years old'})
    return value

class CustomPageNumberPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'page_size': self.page_size,
            'count': self.page.paginator.count,
            'total_pages' : self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })