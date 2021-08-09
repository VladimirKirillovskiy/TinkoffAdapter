from django.urls import path
from adapter.views import MarketDetail, MarketCurrenciesDetail
from rest_framework.authtoken.views import obtain_auth_token
import adapter.views as ad

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/<str:ticker>', ad.MarketDetail.as_view(), name='first'),
    path('market/currencies/<str:currency>', ad.MarketCurrenciesDetail.as_view(), name='currencies'),
]