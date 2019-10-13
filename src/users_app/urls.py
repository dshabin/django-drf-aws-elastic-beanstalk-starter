from django.urls import path,include
from .views import *

urlpatterns = [
    path('', UsersAPIView.as_view()),
    path('<int:id>/', UserAPIView.as_view()),
    path('fetch-current/', FetchCurrentAPIView.as_view()),
]