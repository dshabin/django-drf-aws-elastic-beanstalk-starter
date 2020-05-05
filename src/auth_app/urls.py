from django.urls import path,include
from .views import *

urlpatterns = [
    path('signin/', SigninAPIView.as_view(),name='auth-signin'),
    path('signup/', SignupAPIView.as_view(),name='auth-signup'),
    path('fetch-current/', FetchCurrentAPIView.as_view(),name='auth-fetch-current'),
]