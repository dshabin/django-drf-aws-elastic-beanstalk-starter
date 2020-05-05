from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(),name='auth-login'),
    path('signup/', SignupAPIView.as_view(),name='auth-signup'),
    path('fetch-current/', FetchCurrentAPIView.as_view(),name='auth-fetch-current'),
]