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

    alias = serializers.CharField(
        required=True,
        write_only=True,
    )

    email = serializers.CharField(
        required=True,
        write_only=True,
    )

    # phone_number = serializers.CharField(
    #     required=True,
    #     write_only=True,
    # )

    address = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'alias', 'email', 'password',
                  # 'phone_number',
                  'address')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            alias=validated_data['alias'],
            # phone_number=validated_data['phone_number'],
            address=validated_data['address'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def save(self, request):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            alias=self.validated_data['alias'],
            password=self.validated_data['password'],
            # phone_number=self.validated_data['phone_number'],
            # address=self.validated_data[s'address'],
        )
        return user

    def validate(self, data):
        email = data.get('email', None)
        alias = data.get('alias', None)
        password = data.get('password', None)
        # phone_number = data.get('phone_number', None)
        address = data.get('address', None)

        if email is None:
            raise serializers.ValidationError('Email is required')

        if alias is None:
            raise serializers.ValidationError('alias is required')

        if password is None:
            raise serializers.ValidationError('Password is required')

        # if phone_number is None:
        #     raise serializers.ValidationError('phone_number is required')

        if address is None:
            raise serializers.ValidationError('address is required')

        return data


class UserJWTLoginSerializer(serializers.ModelSerializer):
    alias = serializers.CharField(
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
        fields = ('alias', 'password')

    def validate(self, data):
        alias = data.get('alias', None)
        password = data.get('password', None)

        if User.objects.filter(alias=alias).exists():
            user = User.objects.get(alias=alias)
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
        token['alias'] = user.alias
        # NOTE: cliam에 권한수준에 대한 정보가 들어가야 할 것  같음

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
