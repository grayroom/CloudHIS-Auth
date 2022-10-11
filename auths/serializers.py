from rest_framework import serializers
from auths.models import User, Patient, Doctor

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserJWTSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
        )

        return user

    def save(self, request):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            address=self.validated_data['address'],
        )

        return user

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        name = data.get('name', None)
        email = data.get('email', None)
        phone_number = data.get('phone_number', None)

        if username is None:
            raise serializers.ValidationError('아이디를 입력해주세요')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('이미 사용중인 아이디입니다')

        if password is None:
            raise serializers.ValidationError('비밀번호를 입력해주세요')

        if name is None:
            raise serializers.ValidationError('이름을 입력해주세요')

        if email is None:
            raise serializers.ValidationError('이메일을 입력해주세요')

        if phone_number is None:
            raise serializers.ValidationError('전화번호를 입력해주세요')

        return data


class UserJWTLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)

    password = serializers.CharField(required=True, write_only=True,
                                     style={'input_type': 'password'})

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


class PatientSignupSerializer(UserJWTSignupSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Patient(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],

            doc_idx=validated_data['doc_idx'],
            is_admission=validated_data['is_admission'],
            room=validated_data['room'],
        )

        return user

    def save(self, request):
        user = Patient.objects.create_patient(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            address=self.validated_data['address'],

            doc_idx=self.validated_data['doc_idx'],
            is_admission=self.validated_data['is_admission'],
            room=self.validated_data['room'],
        )

        return user


class DoctorSignupSerializer(UserJWTSignupSerializer):
    room = serializers.CharField(required=False)
    dept_idx = serializers.CharField(required=False)
    sup_idx = serializers.CharField(required=False)

    class Meta:
        model = Doctor
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Doctor(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],

            subject=validated_data['subject'],
            room=validated_data['room'],
            dept_idx=validated_data['dept'],
            sup_idx=validated_data['sup'],
        )

        return user

    def save(self, request):
        user = Doctor.objects.create_doctor(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            address=self.validated_data['address'],

            subject=self.validated_data['subject'],
        )

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        tar = User.objects.get(id=user.id)
        token = super().get_token(tar)

        # Add custom claims
        token['username'] = user.username
        token['authority'] = user.authority
        # NOTE: cliam에 권한수준에 대한 정보가 들어가야 할 것  같음

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
