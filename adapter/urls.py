from django.urls import path
from adapter.views import (MarketDetail, MarketAll)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/all', MarketAll.as_view(), name='marketall'),
    path('market/<str:ticker>', MarketDetail.as_view(), name='first'),
    # path('market/whole', MarketWhole.as_view(), name='wholem'),
]
