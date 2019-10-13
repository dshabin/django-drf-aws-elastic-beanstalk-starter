import traceback
import sys
import json
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import transaction
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import users_serializer, user_serializer
from .permissions import IsUserObjectOwner
from commons.permissions import HasAPIKey, RequestIsPost
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UsersAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [ RequestIsPost | IsAdminUser , ]

    def post(self, request, format=None):
        try:
            params = request.data
            users = User.objects.filter(username=params['username'])
            if users:
                return JsonResponse({"error": {"message": "User already exists."}}, status=200)
            user = User.objects.create_user(**params)
            data = user_serializer(user)
            user = authenticate(username = params['username'], password = params['password'])
            token , _ = Token.objects.get_or_create(user=user)          
            data = user_serializer(user)
            data['token'] = token.key
            return JsonResponse({"data": data}, status=201)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"error": {"message": str(e)}}, status=400)

    def get(self, request, format=None):
        try:
            params = request.GET.dict()
            offset = int(params.get('offset', 0))
            limit = int(params.get('limit', 10))
            order_by = params.get('order_by', 'date_joined')
            order_direction =params.get('order_direction', 'asc')
            params.pop('offset', None)
            params.pop('limit', None)
            params.pop('order_by', None)
            params.pop('order_direction', None)

            order_direction_orm = ''
            if(order_direction == 'desc'):
                order_direction_orm = '-'
            query = {}
            if params.get('search_field',None):
                search_field = params.get('search_field',None)
                search = params.get('search',None)
                search_key = str(search_field)+ '__' + 'contains'
                query[search_key] = search
            print(query)
            result = User.objects.filter(**query).order_by(order_direction_orm+order_by)
            
            count = len(result)
            result = result[offset: offset+limit]
            data = {}
            data['count'] = count
            data['result'] = users_serializer(result)
            return JsonResponse({"data": data}, status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"detail": str(e)}, status=400)


class FetchCurrentAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = []

    def get(self, request, format=None):
        try:
            user = User.objects.get(username=request.user.username)
            data = user_serializer(user)
            return JsonResponse({"data": data}, status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"error": {"message": str(e)}}, status=400)


class UserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserObjectOwner | IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
            data = user_serializer(user)
            return JsonResponse({"data": data}, status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"detail": str(e)}, status=400)

    def put(self, request,  *args, **kwargs):
        try:
            params = request.data
            user = User.objects.get(id=kwargs['id'])
            password = params.pop('password', None)
            if password:
                user.set_password(password)
            for (key, value) in params.items():
                setattr(user, key, value)
            user.save()
            user = User.objects.get(id=kwargs['id'])
            data = user_serializer(user)
            return JsonResponse({"data": data}, status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"detail": str(e)}, status=400)

    def delete(self, request,  *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
            user.delete()
            data = 1
            return JsonResponse({"data": data}, status=200)
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"detail": str(e)}, status=400)
