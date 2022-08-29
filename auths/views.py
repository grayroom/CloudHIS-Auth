from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from auths.serializers import UserJWTSignupSerializer, UserJWTLoginSerializer, CustomTokenObtainPairSerializer

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            # 여기서 유저정보를 serializer를 통해 DB에 저장
            user = serializer.save(request)

            # 토큰 발급
            # TODO: 이걸로 응답도 해야함
            # FIXME: RefreshToken.for_user(user)를 사용하면 안됨!!!! 왜안될까요????
            # token = RefreshToken.for_user(user)
            token = CustomTokenObtainPairSerializer.get_token(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({
                'user': user.username,
                'access': access,
                'refresh': refresh
            })

            # return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
