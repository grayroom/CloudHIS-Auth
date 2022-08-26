from rest_framework import serializers
from auths.models import User


class UserJWTSignupSerializer(serializers.ModelSerializer):
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
        user = super.save()

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
            raise serializers.ValidationError('Username is required')

        if password is None:
            raise serializers.ValidationError('Password is required')

        return data
