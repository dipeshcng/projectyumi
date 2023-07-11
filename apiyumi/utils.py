from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user' : user.username,
        'password' : user.password
    }

class BusinessOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        try:
            usr = user.businessdetail
            if usr.status == "Active":
                has_perm = True
            else:
                has_perm = False
        except Exception as e:
            print(e)
            has_perm = False
        return has_perm

class GraduateOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        try:
            usr = user.graduatesdetail
            if usr.status == "Active":
                has_perm = True
            else:
                has_perm = False
        except Exception as e:
            print(e)
            has_perm = False
        return has_perm