from rest_framework import serializers
from auths.models import User, UserInformation

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserJWTSignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=False,
        write_only=True,
    )

    alias = serializers.CharField(
        required=True,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'alias', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            alias=validated_data['alias'],
            password=validated_data['password'],
            name=validated_data['name']
        )

        return user

    def save(self, request):
        user = User.objects.create_user(
            alias=self.validated_data['alias'],
            password=self.validated_data['password'],
            name=self.validated_data['name']
        )

        return user

    def validate(self, data):
        alias = data.get('alias', None)
        password = data.get('password', None)
        name = data.get('name', None)

        if alias is None:
            raise serializers.ValidationError('alias is required')

        if password is None:
            raise serializers.ValidationError('Password is required')

        if name is None:
            raise serializers.ValidationError('Name is required')

        return data


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = '__all__'

    def create(self, validated_data):
        user_information = UserInformation(
            user_id=validated_data['user_id'],
            name=validated_data['name'],
            email=validated_data['email'],
            address=validated_data['address'],
            subject=validated_data['subject'],
            phone_number=validated_data['phonenumber']
        )

        return user_information

    def save(self, request):
        userinfo = UserInformation.create_user_information(
            user_id=self.validated_data['user_id'],
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            address=self.validated_data['address'],
            subject=self.validated_data['subject'],
            phone_number=self.validated_data['phone_number']
        )

        return userinfo

    def validate(self, data):
        user_id = data.get('user_id', None)
        name = data.get('name', None)
        email = data.get('email', None)
        address = data.get('address', None)
        subject = data.get('subject', None)
        phone_number = data.get('phone_number', None)

        if user_id is None:
            raise serializers.ValidationError('user_id is required')

        if name is None:
            raise serializers.ValidationError('name is required')

        if email is None:
            raise serializers.ValidationError('email is required')

        if address is None:
            raise serializers.ValidationError('address is required')

        if subject is None:
            raise serializers.ValidationError('subject is required')

        if phone_number is None:
            raise serializers.ValidationError('phone_number is required')

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
        tar = User.objects.get(id=user.id)
        token = super().get_token(tar)

        # Add custom claims
        token['alias'] = user.alias
        # NOTE: cliam에 권한수준에 대한 정보가 들어가야 할 것  같음

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
