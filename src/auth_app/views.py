from rest_framework.views import APIView
from django.http import JsonResponse
import traceback
import sys
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from commons.permissions import HasAPIKeyAndRequestIsPost,HasAPIKey
from users_app.serializers import user_serializer

class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        try:
            params = request.data
            username = params['username']
            password = params['password']
            user = authenticate(username = username, password = password)
            if user:
                token , _ = Token.objects.get_or_create(user=user)          
                data = user_serializer(user)
                data['token'] = token.key
            else :
                return JsonResponse({ "error" : {"message"  : "Invalid Username or Password."} },status=200)
            return JsonResponse({"data" : data},status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({ "error" : {"message"  : str(e) } },status=400)
