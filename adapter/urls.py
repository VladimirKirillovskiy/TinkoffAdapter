from django.urls import path
from adapter.views import (MarketDetail, MarketAll)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/stocks/', MarketAll.as_view(), name='marketall'),
    path('market/stocks/<str:ticker>', MarketDetail.as_view(), name='marketstock'),
]
