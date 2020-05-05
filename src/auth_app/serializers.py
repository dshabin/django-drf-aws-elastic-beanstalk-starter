from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username','is_superuser')
        model = User
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True,many=False)
    class Meta:
        fields = '__all__'
        model = Profile

