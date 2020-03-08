import traceback
import sys
import json
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import transaction
from rest_framework.permissions import IsAdminUser
from .models import Profile
from commons.helpers import request_params_parser
from .serializers import ProfileSerializer
from .permissions import IsUserObjectOwner
from commons.permissions import HasAPIKey, RequestIsPost
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UsersAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [ RequestIsPost | IsAdminUser , ]

    def post(self, request, format=None):
        try:
            params = {
                'body_params': {
                    'password': {'required': True},
                    'email' : {'required': True}
                }
            }
            parsed_params = request_params_parser(request, params)
            users = User.objects.filter(username=parsed_params['email'])
            if users:
                return JsonResponse({"error": {"message": "USER_ALREADY_EXIST"}}, status=200)
            user = User.objects.create_user(email=parsed_params['email'],username=parsed_params['email'] , password=parsed_params['password'])
            profile = Profile.objects.create(user=user,)
            token , _ = Token.objects.get_or_create(user=user)          
            data = ProfileSerializer(profile,many=False).data
            data['token'] = token.key
            return JsonResponse({"data": data}, status=201)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"error": {"message": str(e)}}, status=400)


class FetchCurrentAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = []

    def get(self, request, format=None):
        try:
            user = Profile.objects.get(user=request.user)
            data = ProfileSerializer(user,many=False).data
            return JsonResponse({"data": data}, status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"error": {"message": str(e)}}, status=400)

