import jwt
from rest_framework import permissions
from config import settings
from rest_framework_simplejwt.exceptions import TokenError
from auths.authorities import Authority


class IsAuthorizedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        handle_jwt_access_token(request)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            handle_jwt_access_token(request)
        else:
            access_token = request.headers.get("Authorization", None)
            payload = jwt.decode(access_token, settings.SIMPLE_JWT['VERIFYING_KEY'],
                                 algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
            return obj.author == payload.username


def handle_jwt_access_token(request):
    access_token = request.headers.get("Authorization", None)
    try:
        payload = jwt.decode(access_token, settings.SIMPLE_JWT['VERIFYING_KEY'],
                             algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        role = payload['role']
    except (jwt.InvalidTokenError, jwt.DecodeError) as exc:
        raise TokenError(str(exc))

    if role > Authority.NO_AUTHORITY:
        return True
    else:
        return False
