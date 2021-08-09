from django.urls import path
from adapter.views import MarketDetail, Currencies
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/<str:ticker>', MarketDetail.as_view(), name='first'),
    # path('currency/', Currencies.as_view(), name='currency'),
    path('currency/<str:currency>', Currencies.as_view(), name='currency')
]
