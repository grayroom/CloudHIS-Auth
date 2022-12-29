from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework_simplejwt.tokens import RefreshToken

from auths.serializers import UserJWTSignupSerializer, \
    UserJWTLoginSerializer, CustomTokenObtainPairSerializer, \
    DoctorSignupSerializer, PatientSignupSerializer

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from auths.models import User, Patient, Doctor
from config import settings

from auths.permissions import IsAuthorizedUser

import jwt


class HomeView(TemplateView):
    template_name = 'index.html'


class JWTSignupView(APIView):
    doctor_serializer_class = DoctorSignupSerializer
    patient_serializer_class = PatientSignupSerializer

    def post(self, request):
        if (request.data['user_type'] == 'patient'):

            patient_serializer = self.patient_serializer_class(
                data=request.data)

            if patient_serializer.is_valid(raise_exception=False):
                user = patient_serializer.save(request)

                token = CustomTokenObtainPairSerializer.get_token(user)
                refresh = str(token)
                access = str(token.access_token)

                return JsonResponse({
                    'user': user.username,
                    'access': access,
                    'refresh': refresh
                })
            else:
                return Response(patient_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
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
    patientModel = Patient.objects
    doctorModel = Doctor.objects
    permission_classes([IsAuthorizedUser])

    def get(self, request):
        payload = get_payload(request)
        print(payload)

        if (payload['user_type'] == 'patient'):
            user = self.patientModel.get(username=payload['username'])
            return JsonResponse({
                'user': user.username,
                'name': user.name,
                'email': user.email,
                'phone_num': user.phone_number.as_national,
                'address': user.address.split("$")[0],
                'address2': user.address.split("$")[1],
                'user_type': user.user_type
            }, status=status.HTTP_200_OK)
        else:
            user = self.doctorModel.get(username=payload['username'])
            return JsonResponse({
                'user': user.username,
                'name': user.name,
                'email': user.email,
                'phone_num': user.phone_number.as_national,
                'address': user.address.split("$")[0],
                'address2': user.address.split("$")[1],
                'user_type': user.user_type,
                'subject': user.subject,
            }, status=status.HTTP_200_OK)

    def post(self, request):
        payload = get_payload(request)
        if (payload['user_type'] == 'patient'):
            user = self.patientModel.get(username=payload['username'])

            user.email = request.data['email']
            user.phone_number = request.data['phone_num']
            user.address = request.data['address']
            user.save()

            return Response(status=status.HTTP_200_OK)
        else:
            user = self.doctorModel.get(username=payload['username'])

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


class PatientInChargeView(APIView):
    patientModel = Patient.objects
    permission_classes([IsAuthorizedUser])

    def post(self, request):
        doc_idx = request.data['doctor_idx']
        patient_list = self.patientModel.filter(doc_idx=doc_idx)
        patient_serializer = PatientSignupSerializer(patient_list, many=True)
        patient_serializer.is_valid(raise_exception=True)
        # TODO: 여기서 empty exception뜨는데, patient user 추가후에 다시 검증

        # TODO: patient_list -> serializer 구현할 것
        return Response({
            'patient_list': patient_serializer.validated_data
        }, status=status.HTTP_200_OK)
