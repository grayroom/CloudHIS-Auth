from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework_simplejwt.tokens import RefreshToken

from auths.serializers import UserJWTSignupSerializer, UserJWTLoginSerializer, CustomTokenObtainPairSerializer, \
    UserInformationSerializer

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'


class JWTSignupView(APIView):
    user_serializer_class = UserJWTSignupSerializer
    userinfo_serializer_class = UserInformationSerializer

    def post(self, request):
        user_serializer = self.user_serializer_class(data=request.data)

        if user_serializer.is_valid(raise_exception=False):
            # 여기서 유저정보를 serializer를 통해 DB에 저장
            user = user_serializer.save(request)

            # FIXME: 이름좀 바꾸자
            # NOTE: request뜯어서 userinfo entity를 추가하기 위한 과정
            pseudo_request = request
            pseudo_request.data['user_id'] = user.id
            userinfo_serializer = self.userinfo_serializer_class(
                data=pseudo_request.data)
            if userinfo_serializer.is_valid(raise_exception=False):
                userinfo = userinfo_serializer.save(pseudo_request)
            else:
                return Response(userinfo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            token = CustomTokenObtainPairSerializer.get_token(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({
                'user': user.alias,
                'access': access,
                'refresh': refresh
            })
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                'user': user.alias,
                'access': access,
                'refresh': refresh
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
