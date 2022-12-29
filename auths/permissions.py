import jwt
from rest_framework import permissions
from config import settings
from rest_framework_simplejwt.exceptions import TokenError
from auths.authorities import Authority


class IsAuthorizedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        handle_jwt_access_token(request)

    # FIXME: 실제 사용하는 곳이 있는지 확인해봐야할듯
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            handle_jwt_access_token(request)
        else:
            token = request.headers.get("Authorization", None)
            try:
                if request.match("^Bearer .*", token):
                    access_token = token.split(" ")[1]
                    payload = jwt.decode(access_token,
                                         settings.SIMPLE_JWT['VERIFYING_KEY'],
                                         algorithms=[
                                             settings.SIMPLE_JWT['ALGORITHM']])
                    return obj.author == payload.username
                else:
                    raise Exception("invalid token format error")
            except (jwt.InvalidTokenError, jwt.DecodeError, Exception) as exc:
                raise TokenError(str(exc))


def handle_jwt_access_token(request):
    token = request.headers.get("Authorization", None)
    try:
        if request.match("^Bearer .*", token):
            access_token = token.split(" ")[1]
            payload = jwt.decode(access_token,
                                 settings.SIMPLE_JWT['VERIFYING_KEY'],
                                 algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
            role = payload['authority']
        else:
            raise Exception("invalid token format error")
    except (jwt.InvalidTokenError, jwt.DecodeError, Exception) as exc:
        raise TokenError(str(exc))

    if role > Authority.NO_AUTHORITY:
        return True
    else:
        return False
