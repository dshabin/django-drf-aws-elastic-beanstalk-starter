
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
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class SignupAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        try:
            params = {
                'body_params': {
                    'password': {'required': True},
                    'username' : {'required': True}
                }
            }
            parsed_params = request_params_parser(request, params)
            users = User.objects.filter(username=parsed_params['username'])
            if users:
                return JsonResponse({"error": {"message": "USER_ALREADY_EXIST"}}, status=400)
            user = User.objects.create_user(username=parsed_params['username'] , password=parsed_params['password'])
            profile = Profile.objects.create(user=user,)
            data = ProfileSerializer(profile,many=False).data
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
            token , _ = Token.objects.get_or_create(user=request.user) 
            data['token'] = token.key
            return JsonResponse({"data": data}, status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"error": {"message": str(e)}}, status=400)



class SigninAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        try:
            params = {
                'body_params': {
                    'username' : { 'required' : True  },
                    'password' : { 'required' : True  },
                }
            }
            parsed_params = request_params_parser(request,params)
            username = parsed_params['username']
            password = parsed_params['password']
            user = authenticate(username = username, password = password)
            if user:
                token , _ = Token.objects.get_or_create(user=user)
                profile = Profile.objects.get(user=user)         
                data = ProfileSerializer(profile,many=False).data
                data['token'] = token.key
            else :
                return JsonResponse({ "error" : {"message"  : "INAVLID_USERNAME_OR_PASSWORD"} },status=400)
            return JsonResponse({"data" : data},status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({ "error" : {"message"  : str(e) } },status=400)
