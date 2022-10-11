from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework_simplejwt.tokens import RefreshToken

from auths.serializers import UserJWTSignupSerializer, \
    UserJWTLoginSerializer, CustomTokenObtainPairSerializer, \
    DoctorSignupSerializer

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from auths.models import User
from config import settings

from auths.permissions import IsAuthorizedUser

import jwt


class HomeView(TemplateView):
    template_name = 'index.html'


class JWTSignupView(APIView):
    doctor_serializer_class = DoctorSignupSerializer

    def post(self, request):
        doctor_serializer = self.doctor_serializer_class(data=request.data)

        if doctor_serializer.is_valid(raise_exception=False):
            user = doctor_serializer.save(request)

            token = CustomTokenObtainPairSerializer.get_token(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({
                'user': user.username,
                'access': access,
                'refresh': refresh
            })
        else:
            return Response(doctor_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class JWTLoginView(APIView):
    serializer_class = UserJWTLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        # is_valid
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']

            return JsonResponse({
                'user': user.username,
                'access': access,
                'refresh': refresh
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserInformationView(APIView):
    userModel = User.objects
    permission_classes([IsAuthorizedUser])

    def get(self, request):
        payload = get_payload(request)
        user = self.userModel.get(username=payload['username'])

        return JsonResponse({
            'user': user.username,
            'name': user.name,
            'email': user.email,
            'phone_num': user.phone_number.as_national,
            'address': user.address.split("$")[0],
            'address2': user.address.split("$")[1]
        }, status=status.HTTP_200_OK)

    def post(self, request):
        payload = get_payload(request)
        user = self.userModel.get(username=payload['username'])

        user.email = request.data['email']
        user.phone_number = request.data['phone_num']
        user.address = request.data['address']
        user.save()

        return Response(status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes([IsAuthorizedUser])

    def post(self, request):
        refresh = request.COOKIES.get('refresh')
        token = RefreshToken(refresh)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)


def get_payload(req):
    token = req.headers.get("Authorization", None)
    access_token = token.split(" ")[1]
    return jwt.decode(access_token,
                      settings.SIMPLE_JWT['VERIFYING_KEY'],
                      algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
