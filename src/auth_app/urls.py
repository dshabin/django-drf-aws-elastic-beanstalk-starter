from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/', LoginApiView.as_view()),
]