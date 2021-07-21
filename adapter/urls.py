from django.contrib import admin
from django.urls import path
from .views import (HelloView, HelloEveryView)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('helloevery/', HelloEveryView.as_view(), name='helloevery'),
]
