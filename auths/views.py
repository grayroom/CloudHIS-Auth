from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from auths.serializers import UserJWTSignupSerializer

# Create your views here.


class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            # 여기서 유저정보를 serializer를 통해 DB에 저장
            user = serializer.save(request)

            # 토큰 발급
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({
                'user': user,
                'access': access,
                'refresh': refresh
            })
