from rest_framework import serializers
from auths.models import User

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserJWTSignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=False,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    username = serializers.CharField(
        required=True,
        write_only=True,
    )

    email = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def save(self, request):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            password=self.validated_data['password']
        )
        return user

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('Email is required')

        if username is None:
            raise serializers.ValidationError('username is required')

        if password is None:
            raise serializers.ValidationError('Password is required')

        return data


class UserJWTLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        write_only=True
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError('Incorrect password')
        else:
            raise serializers.ValidationError('User does not exist')

        token = CustomTokenObtainPairSerializer.get_token(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'user': user,
            'refresh': refresh,
            'access': access
        }

        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # FIXME: ValueError: Cannot assign "<User: jeonghoon>": "OutstandingToken.user" must be a "User" instance.
        # blacklist 앱 추가할 경우 위와같은 에러 발생
        tar = User.objects.get(id=user.id)
        token = super().get_token(tar)

        # Add custom claims
        token['username'] = user.username
        # NOTE: cliam에 권한수준에 대한 정보가 들어가야 할 것  같음

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
