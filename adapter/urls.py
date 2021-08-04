from django.urls import path
from adapter.views import MarketDetail
from adapter.views import MarketCurrencies
from adapter.views import QuartEarnings
from adapter.views import NextEarns
from adapter.views import Info
from adapter.views import Dividends
from adapter.views import NextDivs
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/currencies', MarketCurrencies.as_view(), name='currencies'),
    path('stock/earn/<str:ticker_name>', QuartEarnings.as_view(), name='earnings'),
    path('stock/nextearns/<str:ticker_name>', NextEarns.as_view(), name='next earnings'),
    path('stock/info/<str:ticker_name>', Info.as_view(), name='info'),
    path('stock/dividends/<str:ticker_name>', Dividends.as_view(), name='dividends'),
    path('stock/nextdivs/<str:ticker_name>', NextDivs.as_view(), name='next dividends'),
    path('market/<str:ticker>', MarketDetail.as_view(), name='first')
]
