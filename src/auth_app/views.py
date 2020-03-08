from rest_framework.views import APIView
from django.http import JsonResponse
import traceback
import sys
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from commons.permissions import HasAPIKeyAndRequestIsPost,HasAPIKey
from users_app.serializers import ProfileSerializer
from commons.helpers import request_params_parser
from users_app.models import Profile
class LoginApiView(APIView):
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
                return JsonResponse({ "error" : {"message"  : "INAVLID_USERNAME_OR_PASSWORD"} },status=200)
            return JsonResponse({"data" : data},status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({ "error" : {"message"  : str(e) } },status=400)
